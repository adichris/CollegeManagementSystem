from django.shortcuts import reverse, get_object_or_404
from django.views.generic import UpdateView, CreateView
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import EmploymentHistoryModel, User
from .forms import EmploymentHistoryCreationForm
from admission.models import StudentForms, FormStatusChoice
from INSTITUTION.utils import get_admission_steps, get_next_url, get_back_url


class EmploymentHistoryCreateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = EmploymentHistoryModel
    form_class = EmploymentHistoryCreationForm
    template_name = 'employment_history/create_view.html'
    permission_required = ('empoymentHistory.add_employmenthistorymodel',
                           'empoymentHistory.change_employmenthistorymodel')
    permission_denied_message = 'You need permission to add or change employment history'

    def get_context_data(self, **kwargs):
        ctx = super(EmploymentHistoryCreateUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Employment History'
        ctx['subtitle'] = 'Employment History (Optional)'
        ctx['step'] = 3
        ctx['steps'] = get_admission_steps(self.request.user.student_profile.admission_form.status)
        ctx["serial_number"] = self.request.user.identity
        return ctx

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def get_object(self, queryset=None):
        instance, _ = EmploymentHistoryModel.objects.get_or_create(
            employee=self.request.user
        )
        return instance

    def form_valid(self, form):
        returns = super(EmploymentHistoryCreateUpdateView, self).form_valid(form)
        admission_form = StudentForms.objects.get(serial_number=self.request.user.identity)
        admission_form.status = FormStatusChoice.AT_SPONSOR
        admission_form.save()

        return returns

    def get_success_url(self):
        return reverse('Student:admission-redirect', kwargs={'serial_number': self.request.user.identity})


class UserEmploymentHistoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'employmenthistory.add_employmenthistorymodel'
    model = EmploymentHistoryModel
    permission_denied_message = 'You need permission to add employment hispry'
    form_class = EmploymentHistoryCreationForm
    template_name = 'employment_history/staff/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserEmploymentHistoryCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Employment History'
        ctx['header'] = 'Employment History'
        return ctx

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(employee__slug=self.kwargs['profile_slug'])
        except self.model.DoesNotExist:
            pass

    def get_profile(self, queryset=None):
        try:
            return User.objects.get(slug=self.kwargs['profile_slug'])
        except User.DoesNotExist:
            pass

    def get_form_kwargs(self):
        kwargs = super(UserEmploymentHistoryCreateView, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.instance.employee = self.get_profile()
        return super(UserEmploymentHistoryCreateView, self).form_valid(form)

    def get_success_url(self):
        next_url = get_next_url(self.request) or get_back_url(self.request)
        if next_url:
            return next_url
        else:
            return super(UserEmploymentHistoryCreateView, self).get_success_url()


@login_required
def get_employment_history_ajax(request, profile_slug):
    user = get_object_or_404(User, slug=request.user.slug)
    if user.is_admin or user.is_superuser:
        user = get_object_or_404(User, slug=profile_slug)
    data = {
        'description': 'Please try again.'
    }
    if user.has_perm('empoymentHistory.view_own_history'):
        try:
            eh_instance = EmploymentHistoryModel.objects.get(employee=user)
        except EmploymentHistoryModel.DoesNotExist:
            data = {
                'description': 'You have no employment history associated to your profile'
            }
        else:
            if eh_instance.has_history or eh_instance.job_title:
                data = {
                    'hasHistory': eh_instance.has_history,
                    'companyName': eh_instance.company_name,
                    'address': eh_instance.address,
                    'state': eh_instance.state,
                    'city': eh_instance.city,
                    'specific_duty': eh_instance.specific_duty,
                    'jobTitle': eh_instance.job_title,
                    'supervisor': eh_instance.supervisor,
                    'employedFrom': eh_instance.employed_from,
                    'employedTo': eh_instance.employed_to,
                    'whyLeave': eh_instance.why_leave
                }
            else:
                data = {
                    'hasHistory': False,
                    'description': 'You do not have any employment history.'
                }
    else:
        data['description'] = 'You need permission to view the employment history'
    return JsonResponse(data)

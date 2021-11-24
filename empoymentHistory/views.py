from django.shortcuts import reverse
from django.views.generic import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import EmploymentHistoryModel
from .forms import EmploymentHistoryCreationForm
from admission.models import StudentForms, FormStatusChoice
from INSTITUTION.utils import get_admission_steps


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
        ctx['subtitle'] = 'Employment History'
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

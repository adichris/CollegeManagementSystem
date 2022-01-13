from django.shortcuts import reverse, get_object_or_404
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AddressCreationForm
from address.models import Address, User
from admission.models import StudentForms, FormStatusChoice
from INSTITUTION.utils import get_admission_steps, get_next_url, get_back_url


class StudentAddressCreateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'address/student/create.html'
    permission_required = ['address.add_address', 'address.change_address']
    form_class = AddressCreationForm
    model = Address
    permission_denied_message = 'Sorry you can not add or change address.'

    def get_context_data(self, **kwargs):
        ctx = super(StudentAddressCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Address'
        ctx["step"] = 2
        ctx["steps"] = get_admission_steps(self.request.user.student_profile.admission_form.status)
        ctx["subtitle"] = 'Your Address'
        ctx['serial_number'] = self.request.user.identity
        return ctx

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def form_valid(self, form):
        form_valid = super(StudentAddressCreateView, self).form_valid(form)
        admission = StudentForms.objects.get(serial_number=self.request.user.identity)
        if admission.status == FormStatusChoice.AT_ADDRESS:
            admission.status = FormStatusChoice.AT_EMPLOYMENT
            admission.save()
        return form_valid

    def get_success_url(self):
        return reverse('Student:admission-redirect', kwargs={'serial_number': self.request.user.identity})

    def get_object(self, queryset=None):
        instance, _ = Address.objects.get_or_create(
            profile_id=self.request.user.id
        )
        return instance


class UserAddressCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Address
    form_class = AddressCreationForm
    permission_required = 'address.add_address'
    permission_denied_message = 'You need permission to add address'
    template_name = 'address/staff/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserAddressCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Address'
        ctx['header'] = 'Address'
        ctx['back_url'] = self.request.GET.get('back')
        return ctx

    def get_object(self):
        try:
            return Address.objects.get(profile__slug=self.kwargs['profile_slug'])
        except Address.DoesNotExist:
            pass

    def get_profile(self):
        return get_object_or_404(User, slug=self.kwargs['profile_slug'])

    def get_form_kwargs(self):
        kwargs = super(UserAddressCreateView, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.instance.profile = self.get_profile()
        return super(UserAddressCreateView, self).form_valid(form)

    def get_success_url(self):
        next_url = get_next_url(self.request)
        if next_url: return next_url
        else:
            return super(UserAddressCreateView, self).get_success_url()

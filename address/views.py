from django.shortcuts import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AddressCreationForm
from address.models import Address
from admission.models import StudentForms, FormStatusChoice
from INSTITUTION.utils import get_admission_steps


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

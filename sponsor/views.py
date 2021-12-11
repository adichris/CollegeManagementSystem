from django.shortcuts import get_object_or_404, reverse
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import StudentSponsor
from .forms import StudentSponsorCreationForm
from student.models import Student
from admission.models import FormStatusChoice
from INSTITUTION.utils import get_admission_steps, get_next_url


class StudentSponsorCreateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('sponsor.add_studentsponsor', 'sponsor.change_studentsponsor')
    model = StudentSponsor
    form_class = StudentSponsorCreationForm
    template_name = 'sponsor/student/admission/create.html'
    permission_denied_message = 'You need permission to add or change sponsor information'

    def get_object(self, queryset=None):
        instance, created = self.model.objects.get_or_create(
            student_id=get_object_or_404(Student, profile_id=self.request.user.id).id
        )
        return instance

    def form_valid(self, form):
        returns = super(StudentSponsorCreateView, self).form_valid(form)
        admission_form = self.get_object().student.admission_form
        admission_form.status = FormStatusChoice.AT_PROGRAMME
        admission_form.save()

        return returns

    def get_context_data(self, **kwargs):
        ctx = super(StudentSponsorCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Admission Sponsor'
        ctx['subtitle'] = ctx['title']
        ctx['step'] = 4
        ctx['steps'] = get_admission_steps(self.request.user.student_profile.admission_form.status)
        ctx['serial_number'] = self.request.user.identity
        return ctx

    def get_success_url(self):
        return reverse('Student:admission-redirect', kwargs={
            "serial_number": self.request.user.identity
        })


class StaffSponsorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('sponsor.add_studentsponsor', 'sponsor.change_studentsponsor')
    model = StudentSponsor
    form_class = StudentSponsorCreationForm
    template_name = 'sponsor/staff/create.html'
    permission_denied_message = 'You need permission to add or change sponsor information'

    def get_object(self, queryset=None):
        try:
            return self.get_student().student_sponsored
        except ObjectDoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        ctx = super(StaffSponsorCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Change Sponsor' if self.get_object() else 'Add Sponsor'
        ctx['header'] = 'Sponsorship'
        ctx['back_url'] = self.request.GET.get('back')
        return ctx

    def get_student(self):
        try:
            return Student.objects.get(
                    index_number=self.kwargs['index_number']
            )
        except Student.DoesNotExist:
            return Http404('The student you want to add sponsorship information does not exist')

    def form_valid(self, form):
        form.instance.student = self.get_student()
        return super(StaffSponsorCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(StaffSponsorCreateView, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return get_next_url(self.request) or super(StaffSponsorCreateView, self).get_success_url()

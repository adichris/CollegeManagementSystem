from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# Create your views here.

from .models import StudentSponsor
from .forms import StudentSponsorCreationForm
from student.models import Student
from admission.models import FormStatusChoice


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
        admission_form = self.get_object().admission_form
        admission_form.status = FormStatusChoice.AT_PROGRAMME
        admission_form.save()

        return returns

    def get_context_data(self, **kwargs):
        ctx = super(StudentSponsorCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Admission Sponsor'
        ctx['subtitle'] = ctx['title']
        ctx['step'] = 4
        ctx['steps'] = tuple(range(1, 5, 1))
        ctx['serial_number'] = self.request.user.identity
        return ctx

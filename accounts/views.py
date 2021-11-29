from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login
from .forms import (
    UserProfileForm
)
from student.models import Student
from .models import User
from INSTITUTION.utils import get_admission_steps


class StudentProfileCreateView(View):
    template_name = 'accounts/student/create_view.html'
    form_class = UserProfileForm
    model = User

    def get_object(self):
        return self.model.objects.filter(
            identity=self.kwargs['serial_number'],
            is_online=True,
        ).first()

    def get_success_url(self):
        return redirect('Student:admission-redirect',
                        serial_number=self.kwargs['serial_number'],
                        )

    def get_context_data(self):
        try:
            steps = get_admission_steps(self.request.user.student_profile.admission_form.status)
        except AttributeError:
            steps = (1, )
        return {
            "step": 1,
            "subtitle": 'Personal Information',
            "steps": steps,
            'serial_number': self.kwargs['serial_number'],
        }

    def get_initial(self):
        return {
            'identity': self.kwargs["serial_number"]
        }

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        ctx['serial_number'] = self.kwargs['serial_number']
        ctx["form"] = self.form_class(instance=self.get_object(), initial=self.get_initial())
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        user_instance = self.get_object()
        profile_form = self.form_class(
            request.POST,
            files=request.FILES,
            initial=self.get_initial(),
            instance=user_instance)

        if profile_form.is_valid():
            profile = profile_form.save()
            admission_form = self.update_admission_status()
            if not user_instance:
                profile.identity = admission_form.serial_number
                profile.save()
            if not request.user.is_authenticated or request.user != profile:
                login(self.request, user=profile)
            return redirect('Student:admission-redirect', serial_number=admission_form.serial_number)
        ctx['form'] = profile_form
        return render(request, self.template_name, ctx)

    def update_admission_status(self):
        from admission.models import FormStatusChoice, StudentForms
        admission_form = get_object_or_404(
            StudentForms,
            serial_number=self.kwargs["serial_number"]
        )
        if not admission_form.status or admission_form.status == FormStatusChoice.NEW:
            admission_form.status = FormStatusChoice.AT_ADDRESS
            admission_form.save()
        return admission_form


class ContinuouStudentProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'accounts.add_user'
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/staff/create_continuous.html'

    def get_context_data(self):
        return {
            'title': 'Add Profile',
        }

    def get_success_url(self):
        return reverse('Student:staff_register_student', kwargs={
            'index_number': self.kwargs['index_number']
        })

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        student = self.get_student()
        ctx['form'] = self.form_class(instance=student.profile)
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        student = self.get_student()
        form_class = self.form_class(self.request.POST, files=request.FILES, instance=student.profile)
        if form_class.is_valid():
            profile = form_class.save(False)
            profile.identity = self.kwargs['index_number']
            profile.save()
            student.profile = profile
            student.save()
            return redirect('Student:staff_register_student', index_number=student.index_number, permanent=True)
        ctx['form'] = form_class
        return render(request, self.template_name, ctx)

    def get_student(self):
        return get_object_or_404(Student, index_number=self.kwargs['index_number'])

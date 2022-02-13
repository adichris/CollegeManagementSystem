from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import View, UpdateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout

from lecture.models import Lecturer
from .forms import (
    UserProfileForm,
    SetPasswordForm
)
from student.models import Student
from .models import User
from INSTITUTION.utils import get_admission_steps, get_back_url, get_next_url
from INSTITUTION.views import JsonResponseMixin


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
        try:
            return Student.objects.get(
               index_number=self.kwargs['index_number']
            )
        except Student.DoesNotExist:
            raise Http404('The student your operating on does not exists')


class LecturerProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/lecturer/create.html'
    permission_required = 'accounts.add_lecturerprofile'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Add Lecture Profile',
        }
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        ctx['form'] = self.form_class(instance=self.get_profile_instance())
        return render(request, self.template_name, ctx)
    
    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, files=request.FILES, instance=self.get_profile_instance())
        if form_class.is_valid():
            profile_instance = form_class.save(False)
            lecturer = self.get_lecturer()
            profile_instance.identity = lecturer.identity
            profile_instance.save()
            if not lecturer.profile:
                lecturer.profile = profile_instance
                lecturer.save()
            return redirect('Lecturer:staff_add_template', identity=lecturer.identity)
        ctx = self.get_context_data()
        ctx['form'] = form_class
        return render(request, self.template_name, ctx)
    
    def get_lecturer(self):
        try:
            self.lecturer = Lecturer.objects.get(
                identity = self.kwargs['identity']
            )
            return self.lecturer
        except Lecturer.DoesNotExist:
            raise Http404('The lecturer does not exist in the system')

    def get_profile_instance(self):
        try:
            return User.objects.get(
                identity=self.kwargs['identity']
            )    
        except User.DoesNotExist:
            return


class SetPassword4other(LoginRequiredMixin, PermissionRequiredMixin, JsonResponseMixin, UpdateView):
    permission_required = 'accounts.set_password4other'
    permission_denied_message = 'you need permission to set password for other user'
    form_class = SetPasswordForm
    model = User
    template_name = 'accounts/staff/create_continuous.html'

    def get_object(self, queryset=None):
        try:
            return User.objects.get(identity=self.kwargs['identity'])
        except User.DoesNotExist:
            raise Http404('User can not be found!')

    def get_success_data(self):
        response = super(SetPassword4other, self).get_success_data()
        response['has_password'] = True
        return response

    def get_success_url(self):
        return self.request.path


class SetNewPassword(LoginRequiredMixin, UpdateView):
    form_class = SetPasswordForm
    model = User
    template_name = 'accounts/setpassword.html'

    def get_success_url(self):
        nxt = get_next_url(self.request)
        if nxt:
            return nxt
        if self.request.user.student:
            return reverse(self.request.user.student)
        else:
            return logout(self.request)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super(SetNewPassword, self).get_context_data(**kwargs)
        ctx['title'] = 'Set a new password'
        ctx['back'] = get_back_url(self.request)
        return ctx


def logout_to_homepage(request):
    logout(request)
    return redirect('Home:landing_page')

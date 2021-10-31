from django.shortcuts import get_object_or_404, reverse, render
from django.views.generic import RedirectView, View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from accounts.models import User
from django.contrib.auth.models import Permission, Group
from django.forms import modelformset_factory

from .models import (
    Student,
    CertExamRecord,
    AdmissionCertificate,
    )
from admission.models import StudentForms, FormStatusChoice
from .forms import (
    ProgrammeSelectionChangeForm,
    StudentProgrammeChoice,
    CertExamRecordForm
)


class StudentAdmissionRedirectView(RedirectView):
    #  check the admission status and redirect the student to the require path

    def get_redirect_url(self, *args, **kwargs):
        admission_form = get_object_or_404(StudentForms, serial_number=self.kwargs['serial_number'])
        if admission_form.status == FormStatusChoice.NEW:
            return reverse('Accounts:admission_student_profile', kwargs={
                "serial_number": admission_form.serial_number
            })

        if admission_form.status != FormStatusChoice.Expired:
            user = User.objects.get(identity=admission_form.serial_number)
            if self.request.user != user:
                if self.request.user.is_authenticated:
                    logout(request=self.request)
                login(user=user, request=self.request)

            student, created_student = Student.objects.get_or_create(
                admission_form_id=admission_form.id, profile_id=user.id
            )
            self.set_permissions_required()

            if admission_form.status == FormStatusChoice.AT_ADDRESS:
                return reverse('Address:admission_student_create')

            elif admission_form.status == FormStatusChoice.AT_EMPLOYMENT:
                return reverse('EmploymentHistory:student_admission_create_history')

            elif admission_form.status == FormStatusChoice.AT_SPONSOR:
                return reverse('Sponsor:student_admission')

            elif admission_form.status == FormStatusChoice.AT_PROGRAMME:
                return reverse('Student:programmes_choices')

        elif admission_form.status == FormStatusChoice.COMPLETED:
            pass

        else:
            pass

    def set_permissions_required(self):
        student_admission_grp, created = Group.objects.get_or_create(name='student admission')
        student_admission_grp.permissions.add(*Permission.objects.filter(
            codename__in=('add_employmenthistorymodel',
                          'change_employmenthistorymodel',
                          'add_studentsponsor',
                          'change_studentsponsor',
                          'add_address',
                          'change_address',
                          'view_programme',
                          'view_student',
                          )
            ),
                                              )
        self.request.user.groups.add(student_admission_grp)


class StudentProgrammeSelectionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('programme.view_programme', 'student.view_student')
    model = Student
    form_class = ProgrammeSelectionChangeForm
    template_name = 'student/admission/create.html'
    permission_denied_message = 'You need permission to view programmes'

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def get_context_data(self, **kwargs):
        return {
            'title': 'Programmes Choices',
            'step': 5,
            'steps': range(1, 6),
            'serial_number': self.request.user.identity,
            'subtitle': '3 programme of choice'
        }

    def get_object(self):
        student_choice_model = StudentProgrammeChoice.objects.filter(student__profile=self.request.user)
        return student_choice_model.first()

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class(
            instance=self.get_object()
        )
        ctx = self.get_context_data()
        ctx['form'] = form_instance
        return render(self.request, self.template_name, context=ctx)

    def post(self, request, *args, **kwargs):
        programmes_choices_instance = self.get_object()
        form_instance = self.form_class(data=request.POST, instance=programmes_choices_instance)
        ctx = self.get_context_data()
        if form_instance.is_valid():
            if programmes_choices_instance:
                instance = form_instance.save(True)
            else:
                programmes_choices_instance = form_instance.save(False)
                student_instance = Student.objects.get(profile_id=self.request.user.id)
                programmes_choices_instance.student_id = student_instance.id
                programmes_choices_instance.save()
        ctx['form'] = form_instance
        return render(self.request, self.template_name, context=ctx)


class AdmissionCertificate(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = CertExamRecord
    formset_class = modelformset_factory(
        model=model, 
        form=CertExamRecordForm, 
        max_num=20, 
        validate_max=True, 
        extra=1,
        min_num=6,
        validate_min=True,
        )
    permission_required = ('student.add_certexamrecord', 'student.change_certexamrecord')
    permission_denied_message = 'You need permission to add and change student admission certificate exam records'
    template_name = 'student/admission/create.html'

    def get_context_data(self):
        return {
            'title': 'Certificate',
            'subtitle': 'Certificate Records',
            'step':7,
            'steps': range(1, 8),
            'serial_number':self.request.user.identity,
        }
    
    def get(self, request, *args, **kwargs):
        content = self.get_context_data()
        content['form'] = self.formset_class(queryset=self.get_certificate_queryset())
        return render(
            request=request,
            template_name=self.template_name,
            context=content,
        )
    
    def get_certificate_queryset(self):
        return 


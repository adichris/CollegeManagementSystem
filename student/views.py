from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.views.generic import RedirectView, View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.forms import modelformset_factory
from django.db import IntegrityError

from accounts.models import User
from .models import (
    Student,
    CertExamRecord,
    AdmissionCertificate,
    StudentPreviousEducation,
    )
from admission.models import StudentForms, FormStatusChoice
from .forms import (
    ProgrammeSelectionChangeForm,
    StudentProgrammeChoice,
    CertExamRecordForm,
    StudentPreviousEducationChangeForm,
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

            elif admission_form.status == FormStatusChoice.AT_CERTIFICATION:
                return reverse('Student:admission_cert_exam_records')

            elif admission_form.status == FormStatusChoice.AT_EDUCATION:
                return reverse('Student:admission_previous_education')

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
                          'add_certexamrecord',
                          'change_certexamrecord',
                          'add_studentpreviouseducation',
                          'change_studentpreviouseducation',
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
            student_instance = Student.objects.get(profile_id=self.request.user.id)
            if programmes_choices_instance:
                instance = form_instance.save(True)
            else:
                programmes_choices_instance = form_instance.save(False)
                programmes_choices_instance.student_id = student_instance.id
                programmes_choices_instance.save()
            admission_form = student_instance.admission_form
            admission_form.status = FormStatusChoice.AT_CERTIFICATION
            admission_form.save()
            return redirect(
                'Student:admission-redirect', serial_number=admission_form.serial_number
            )
        ctx['form'] = form_instance
        return render(self.request, self.template_name, context=ctx)


class AdmissionCertificateExaminationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = CertExamRecord
    formset_class = modelformset_factory(
        model=model, 
        form=CertExamRecordForm, 
        max_num=15,
        validate_max=True, 
        extra=1,
        min_num=6,
        validate_min=True,
        absolute_max=15,
        can_delete=True,
        can_delete_extra=True,
        )
    permission_required = ('student.add_certexamrecord', 'student.change_certexamrecord')
    permission_denied_message = 'You need permission to add and change student admission certificate exam records'
    template_name = 'student/admission/CertExamRecord.html'

    def get_context_data(self):
        return {
            'title': 'Certificate',
            'subtitle': 'Certificate Records',
            'step': 6,
            'steps': range(1, 7),
            'serial_number': self.request.user.identity,
        }
    
    def get(self, request, *args, **kwargs):
        content = self.get_context_data()
        content['formset'] = self.formset_class(
            queryset=self.get_cert_exam_record_queryset(),
            form_kwargs={
                'certificate_id': self.certificate_object.id
            }
        )
        return render(
            request=request,
            template_name=self.template_name,
            context=content,
        )

    def get_cert_exam_record_queryset(self):
        return CertExamRecord.objects.filter(
            certificate=self.get_certificate_object()
        )

    def get_certificate_object(self):
        instance, created = AdmissionCertificate.objects.get_or_create(
            student=Student.objects.get(profile=self.request.user),
        )
        self.certificate_object = instance
        return instance

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        ecr_queryset = self.get_cert_exam_record_queryset()
        formset = self.formset_class(data=request.POST,
                                     queryset=ecr_queryset,
                                     form_kwargs={
                                         'certificate_id': self.certificate_object.id
                                     })
        try:
            if formset.is_valid():
                ecr_instances = formset.save(True)
                # for ecr_instance in ecr_instances:
                #     ecr_instance.certificate_id = self.certificate_object.id
                #     ecr_instance.save()
                # for form2delete in formset.deleted_forms:
                #     form2delete.delete()
                admission_form = self.certificate_object.student.admission_form
                admission_form.status = FormStatusChoice.AT_EDUCATION
                admission_form.save()
                return redirect('Student:admission-redirect',
                                serial_number=admission_form.serial_number)
        except IntegrityError:
            non_field_errors = formset.get_form_error()
            context['integrityError'] = f"""
                There are some duplication or repeated entries in your form,
                check and try again <br/>
                <ul>
                    <li>examination type</li>
                    <li>examination year</li>
                    <li>subject</li>
                </ul>
                <p>{non_field_errors}</p>
                """

        context['formset'] = formset
        return render(request, self.template_name, context)


class StudentPreviousEducationChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = StudentPreviousEducation
    template_name = 'student/admission/create.html'
    permission_required = ('student.add_studentpreviouseducation', 'student.change_studentpreviouseducation')
    form_class = StudentPreviousEducationChangeForm

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def get(self, request, *args, **kwargs):
        ctx = self.get_content_data()
        ctx['form'] = self.form_class()
        return render(request, self.template_name, context=ctx)

    def get_content_data(self):
        return {
            'title': 'Previous Education',
            'step': 7,
            'steps': range(1, 8),
            'serial_number': self.request.user.identity,
            'subtitle': 'Previous Education'
        }

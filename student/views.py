from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.views.generic import RedirectView, View, DetailView, TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.forms import modelformset_factory
from django.db import IntegrityError
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now as today_time

from Home.templatetags.institution_extra import get_institution_fullname_name
from INSTITUTION.utils import get_not_allowed_render_response, get_next_url, get_back_url, get_admission_steps, \
    AcademicYear
from accounts.models import User
from accounts.forms import ChangePasswordForm
from programme.models import Programme
from department.models import Department
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
    StudentCreationForm,
)
from django.conf import settings as APP_SETTINGS

class StudentAdmissionRedirectView(RedirectView):
    #  check the admission status and redirect the student to the require path

    def get_redirect_url(self, *args, **kwargs):
        admission_form = get_object_or_404(StudentForms, serial_number=self.kwargs['serial_number'])
        if admission_form.status == FormStatusChoice.NEW:
            return reverse('Accounts:admission_student_profile', kwargs={
                "serial_number": admission_form.serial_number
            })

        if admission_form.status != FormStatusChoice.EXPIRED:
            try:
                user = User.objects.get(identity=admission_form.serial_number)
            except User.DoesNotExist:
                user = admission_form.student.profile
            except ObjectDoesNotExist:
                raise Http404('Student with such admission serial number does not exists')
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

            elif admission_form.status in (FormStatusChoice.SUBMITTED,
                                           FormStatusChoice.COMPLETED,
                                           FormStatusChoice.ACCEPTED,
                                           ):
                return reverse('Student:admission_detail')

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
    permission_denied_message = 'You need permission to view programmes'

    @property
    def template_name(self):
        if self.is_student:
            return 'student/staff/create.html'
        return 'student/admission/create.html'

    @property
    def is_student(self):
        return self.kwargs.get('index_number')

    def get_login_url(self):
        if self.is_student:
            return reverse('Home:login')
        return reverse('Admission:main_template_page')

    def get_context_data(self,):
        kwargs = {
            'title': 'Programmes Choices',
            'subtitle': '3 programme of choice',
            'back_url': get_back_url(self.request)
        }
        student = self.get_student()
        if self.kwargs.get('index_number'):
            kwargs['reuse'] = True
            kwargs['subtitle'] = 'Should be one of the student current programme'
            kwargs['subtitle2'] = f'({student.programme})'
            kwargs['header'] = 'What where the student programme selection'
        kwargs['step'] = 5
        kwargs['steps'] = get_admission_steps(student.admission_form.status)
        kwargs['serial_number'] = student.admission_form.serial_number
        return kwargs

    def get_object(self):
        index_number = self.kwargs.get('index_number')
        if index_number:
            try:
                return StudentProgrammeChoice.objects.get(
                    student__index_number=index_number
                )
            except StudentProgrammeChoice.DoesNotExist:
                return
        else:
            student_choice_model = StudentProgrammeChoice.objects.filter(student__profile=self.request.user)
            return student_choice_model.first()

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class(
            instance=self.get_object(),
            initial=self.get_initial()
        )
        ctx = self.get_context_data()
        ctx['form'] = form_instance
        return render(self.request, self.template_name, context=ctx)

    def post(self, request, *args, **kwargs):
        programmes_choices_instance = self.get_object()
        form_instance = self.form_class(data=request.POST, instance=programmes_choices_instance, initial=self.get_initial())
        ctx = self.get_context_data()
        if form_instance.is_valid():
            student_instance = self.get_student()
            if programmes_choices_instance:
                form_instance.save(True)
            else:
                programmes_choices_instance = form_instance.save(False)
                programmes_choices_instance.student_id = student_instance.id
                programmes_choices_instance.save()
            admission_form = student_instance.admission_form
            if admission_form:
                admission_form.status = FormStatusChoice.AT_CERTIFICATION
                admission_form.save()
            if self.is_student:
                return redirect(
                    'Student:staff_register_student',
                    index_number=self.kwargs['index_number']
                )
            return redirect(
                'Student:admission-redirect', serial_number=admission_form.serial_number
            )
        ctx['form'] = form_instance
        return render(self.request, self.template_name, context=ctx)

    def get_student(self):
        if self.is_student:
            return Student.objects.get(index_number=self.kwargs['index_number'])
        return Student.objects.get(profile_id=self.request.user.id)

    def get_initial(self):
        if self.is_student and not self.get_object():
            student = self.get_student()
            return {
                'first_choice': student.programme,
                'second_choice': student.programme,
                'third_choice': student.programme,
            }


class AdmissionCertificateExaminationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = CertExamRecord
    formset_class = modelformset_factory(
        model=model,
        form=CertExamRecordForm,
        max_num=15,
        validate_max=True,
        extra=1,
        min_num=7,
        validate_min=True,
        absolute_max=15,
        can_delete=True,
        can_delete_extra=True,
    )
    permission_required = ('student.add_certexamrecord', 'student.change_certexamrecord')
    permission_denied_message = 'You need permission to add and change student admission certificate exam records'
    template_name = 'student/admission/CertExamRecord.html'

    def get_context_data(self):
        if not self.kwargs.get('index_number'):
            steps = get_admission_steps(self.request.user.student_profile.admission_form.status)
        else:
            steps = None
        return {
            'title': 'Certificate Record',
            'subtitle': 'Certificate Records',
            'step': 6,
            'steps': steps,
            'serial_number': self.request.user.identity,
            'col_css_class': 'col-lg-11',
            'legend': 'Subject Form',
            'show_counter': True,
            'back_url': get_back_url(self.request),

        }

    def get(self, request, *args, **kwargs):
        content = self.get_context_data()
        content[self.get_form_name()] = self.formset_class(
            queryset=self.get_cert_exam_record_queryset(),
            form_kwargs={
                'certificate_id': self.certificate_object.id
            }
        )
        return render(
            request=request,
            template_name=self.get_template_name(),
            context=content,
        )

    def get_form_name(self):
        return 'formset'

    def get_template_name(self):
        if self.kwargs.get('index_number'):
            return 'student/staff/add_certificate.html'
        return self.template_name

    def get_cert_exam_record_queryset(self):
        return CertExamRecord.objects.filter(
            certificate=self.get_certificate_object()
        )

    def get_certificate_object(self):
        self.student = self.get_student()
        if self.student:
            instance, created = AdmissionCertificate.objects.get_or_create(
                student=self.student,
            )
        else:
            try:
                self.student = Student.objects.get(profile=self.request.user)
            except Student.DoesNotExist:
                raise Http404('Please reload the page')
            else:
                instance, created = AdmissionCertificate.objects.get_or_create(
                    student=self.student
                )
                self.certificate_object = instance
                return instance

    def get_login_url(self):
        if self.get_student():
            return reverse('Home:login')
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
                ecr_instances = formset.save(False)
                for ecr_instance in ecr_instances:
                    ecr_instance.certificate_id = self.certificate_object.id
                    ecr_instance.save()
                for form2delete in formset.deleted_forms:
                    del form2delete
                admission_form = self.certificate_object.student.admission_form
                if admission_form:
                    admission_form.status = FormStatusChoice.AT_EDUCATION
                    admission_form.save()
                if self.kwargs.get('index_number'):
                    return redirect(get_next_url(request))
                return redirect('Student:admission-redirect',
                                serial_number=admission_form.serial_number)
        except IntegrityError as err:
            non_field_errors = formset.get_form_error()
            if non_field_errors:
                return self.get(request, *args, **kwargs)
            context['integrityError'] = f"""
                There are some duplication or repeated entries in your form,
                check and try again <br/>
                <p>{non_field_errors}</p>
                """
        if formset.errors:
            context['has_errors'] = formset.total_error_count()
            context['err_msg'] = 'Correct the ' + str(context['has_errors']) + ' field(s) marked in <b style="color:red">red</b>'
        context[self.get_form_name()] = formset
        return render(request, self.get_template_name(), context)

    def get_student(self):
        index_number = self.kwargs.get('index_number')
        if index_number:
            try:
                return Student.objects.get(
                    index_number=index_number
                )
            except Student.DoesNotExist:
                raise Http404('The operation not success student does not exist')


class StudentPreviousEducationChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = StudentPreviousEducation
    template_name = 'student/admission/CertExamRecord.html'
    permission_required = ('student.add_studentpreviouseducation', 'student.change_studentpreviouseducation')
    form_class = modelformset_factory(
        model=model,
        form=StudentPreviousEducationChangeForm,
        extra=1,
        max_num=3,
        validate_max=True,
        min_num=1,
        validate_min=True,
        absolute_max=3,
        can_delete=True,
        can_delete_extra=True
    )

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def get(self, request, *args, **kwargs):
        ctx = self.get_content_data()
        ctx['formset'] = self.form_class(
            form_kwargs={
                "student_id": self.request.user.student_profile.id,
            },
            queryset=self.get_queryset()
        )
        return render(request, self.template_name, context=ctx)

    def get_queryset(self):
        return self.model.objects.filter(
            student_id=self.request.user.student_profile.id
        )

    def get_content_data(self):
        return {
            'title': 'Previous Education',
            'step': 7,
            'steps': get_admission_steps(self.request.user.student_profile.admission_form.status),
            'serial_number': self.request.user.identity,
            'subtitle': 'Previous Education',
            'legend': 'Previous school',
            'col_css_class': 'col-md-auto',
            'container_css_class': 'container',
            'show_counter': False,
        }

    def post(self, request, *args, **kwargs):
        ctx = self.get_content_data()
        formset = self.form_class(data=self.request.POST,
                                  form_kwargs={"student_id": self.request.user.student_profile.id},
                                  queryset=self.get_queryset()
                                  )
        if formset.is_valid():
            # formset.save(True)
            instances = formset.save(False)
            for instance in instances:
                instance.save()
            admission_form = self.request.user.student_profile.admission_form
            admission_form.status = FormStatusChoice.COMPLETED
            admission_form.save()
            return redirect('Student:admission-redirect', serial_number=admission_form.serial_number)
        ctx['formset'] = formset
        return render(request, self.template_name, context=ctx)


class StudentAdmissionDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'student/admission/detail.html'
    permission_required = 'student.view_student'
    model = Student

    def get_object(self, queryset=None):
        return self.request.user.student_profile

    def get_context_data(self, **kwargs):
        ctx = super(StudentAdmissionDetails, self).get_context_data(**kwargs)
        ctx['title'] = self.request.user
        ctx['subtitle'] = 'You have successful completed'
        ctx['status_accepted'] = self.status_accepted()
        ctx['notice'] = 'You have been given admission to <b>%s</b>' % get_institution_fullname_name()
        if not self.request.user.password:
            m_form = self.get_password_form()(self.request.user, data=self.request.POST or None)
            # form buttons
            from crispy_forms.helper import FormHelper
            from crispy_forms.bootstrap import StrictButton, FormActions
            helper = FormHelper(m_form)
            helper.layout.append(
                FormActions(
                    StrictButton('Save Password', css_class='btn-primary', onlclick='dynamicSpinner()', type='submit'),
                    StrictButton('Reset', css_class='btn-light', type='reset'),
                )
            )
            helper.form_action = reverse('Accounts:set_pwd')
            m_form.helper = helper
            ctx['m_form'] = m_form
        return ctx

    def get_password_form(self):
        from django.contrib.auth.forms import SetPasswordForm
        return SetPasswordForm

    def status_accepted(self):
        return self.object.admission_form.status == FormStatusChoice.ACCEPTED

    def get(self, request, *args, **kwargs):
        if request.user.password:
            logout(request)
            return redirect('Student:home')
        return super(request, *args, **kwargs)


class StaffStudentTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'student/staff/template.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(StaffStudentTemplateView, self).get(request, *args, **kwargs)
        else:
            return get_not_allowed_render_response(request)

    def get_context_data(self, **kwargs):
        ctx = super(StaffStudentTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Students'
        return ctx


class StaffRegisterStudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = (
    'student.add_student', 'admission.add_studentform', 'accounts.add_user', 'address.add_address')
    template_name = 'student/staff/register.html'
    permission_denied_message = 'You need permission to add students profile, address, admission form'

    def get_student(self):
        try:
            return Student.objects.get(
                index_number=self.kwargs['index_number']
            )
        except Student.DoesNotExist:
            raise Http404('The page your looking for does bot exist.')

    def get_context_data(self, **kwargs):
        ctx = super(StaffRegisterStudentDetailView, self).get_context_data(**kwargs)
        self.student = self.get_student()
        self.profile = self.get_profile()
        ctx['title'] = 'Add Student'
        ctx['back_url'] = get_back_url(self.request)
        ctx['index_number'] = self.student.index_number
        ctx['has_profile'] = bool(self.profile)
        ctx['student_detail4staff'] = self.student.get_absolute_detailview4staff
        if self.profile:
            ctx['profile_slug'] = self.profile.slug
            ctx['name'] = self.profile.get_full_name()
            ctx['has_password'] = self.profile.password
            ctx['has_address'] = self.has_address()
            ctx['has_employment_history'] = self.has_employment_history()
        ctx['department'] = self.student.programme.department
        ctx['has_sponsorship'] = self.has_sponsorship()
        ctx['has_education'] = self.has_previous_education()
        ctx['has_admission_form'] = self.has_admission_form()
        ctx['has_selected_programme'] = self.has_selected_programme()
        ctx['has_cert'] = self.has_certificate()
        ctx['disable_address'] = 'Student profile must be created first in other to add ADDRESS' \
            if not ctx['has_profile'] else None
        ctx['disable_employmenthistory'] = 'Student profile must be created first in other to add EMPLOYMENT HISTORY' \
            if not ctx['has_profile'] else None

        if ctx['has_profile'] and ctx['has_address'] and ctx['has_admission_form'] and ctx['has_cert'] and not self.student.is_active:
            self.student.is_active = True
            self.student.save()
        ctx['is_active'] = self.student.is_active
        return ctx

    def get_profile(self):
        try:
            return self.student.profile
        except ObjectDoesNotExist:
            return False

    def is_student_editable(self):
        pass

    def has_address(self):
        try:
            return bool(self.student.profile.address)
        except ObjectDoesNotExist:
            return False

    def has_employment_history(self):
        try:
            return bool(self.profile.employment_history)
        except ObjectDoesNotExist:
            return False

    def has_sponsorship(self):
        try:
            return bool(self.student.student_sponsored)
        except ObjectDoesNotExist:
            return False

    def has_selected_programme(self):
        try:
            return bool(self.student.programme_choices)
        except ObjectDoesNotExist:
            return False

    def has_certificate(self):
        try:
            return self.student.cert_student.certificate_records.exists()
        except ObjectDoesNotExist:
            return False

    def has_previous_education(self):
        try:
            return self.student.previous_education.exists()
        except ObjectDoesNotExist:
            return False

    def has_admission_form(self):
        try:
            return self.student.admission_form
        except ObjectDoesNotExist:
            return False


class StaffStudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    template_name = 'student/staff/create.html'
    form_class = StudentCreationForm
    permission_denied_message = 'You need permission to add student'
    permission_required = 'student.add_student'

    def get_context_data(self, **kwargs):
        ctx = super(StaffStudentCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Register Student'
        ctx['header'] = 'Register Student'
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def get_success_url(self):
        return reverse('Student:staff_register_student', kwargs={'index_number': self.object.index_number})


class StaffStudentUpdateIndexNumProgrammeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    template_name = 'student/staff/create.html'
    form_class = StudentCreationForm
    permission_required = 'student.change_student'
    permission_denied_message = 'You need permission to change student'

    def get_context_data(self, **kwargs):
        ctx = super(StaffStudentUpdateIndexNumProgrammeUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Index number, and Programme'
        ctx['isto_update'] = True
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def get_success_url(self):
        return get_next_url(self.request) or super(StaffStudentUpdateIndexNumProgrammeUpdateView,
                                                   self).get_success_url()

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(
                index_number=self.kwargs['index_number']
            )
        except self.model.DoesNotExist:
            raise Http404('The student your looking for does not exist')


class StaffSelectStudentProgramme(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'programme.list_programme'
    permission_denied_message = 'You need permission to view programme list'
    model = Programme
    template_name = 'student/staff/programme_list.html'
    programme_search_varname = 'qprogramme'
    student_search_varname = 'qstudent'

    def get_queryset(self):
        q_programme = self.get_programme_search()
        kwargs = {}
        if self.is2_all_student:
            kwargs['student__isnull'] = False
        else:
            kwargs['student__date_admitted__year'] = today_time().year

        if q_programme:
            kwargs['name__icontains'] = q_programme
        return self.model.objects.filter(**kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(StaffSelectStudentProgramme, self).get_context_data(object_list=object_list, **kwargs)
        if self.is2_all_student:
            ctx['title'] = 'All Student \nby Programmes'
        else:
            ctx['title'] = 'New Admitted Student \nby Programmes'
        ctx['header'] = ctx['title']
        ctx['in_tab'] = self.get_in_tab()
        ctx['back_url'] = get_back_url(self.request)
        ctx['p_variable_name'] = self.programme_search_varname
        ctx['s_variable_name'] = self.student_search_varname
        ctx['p_searched'] = self.get_programme_search()
        ctx['s_action'] = self.get_search_student_action()
        ctx['is2_all_student'] = self.is2_all_student
        return ctx

    def get_in_tab(self):
        in_tab = self.request.GET.get('intab') == 't'
        pre_value = self.request.session.get('openintab')
        if in_tab and pre_value:
            self.request.session['openintab'] = False
            return False
        elif in_tab and not pre_value:
            self.request.session['openintab'] = True
            return True
        else:
            return pre_value

    def get_search_student_action(self):
        if self.is2_all_student:
            return reverse('Student:staff_all')
        return reverse('Student:staff_newly_admitted_search')

    @property
    def is2_all_student(self):
        return self.request.GET.get('allstudents') == '1'

    def get_programme_search(self):
        return self.request.GET.get(self.programme_search_varname)

    def get_student_search(self):
        return self.request.GET.get(self.student_search_varname)


class NewlyAdmittedStudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    permission_required = 'student.view_students'
    permission_denied_message = 'You need permission to view newly admitted students list'
    template_name = 'student/staff/newlystudentlist.html'
    query_variable = 'qstudent'

    def get_context_data(self, object_list=None, **kwargs):
        ctx = super(NewlyAdmittedStudentListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'Newly Admitted Student'
        ctx['header'] = 'New Admitted Student'
        if self.kwargs.get('programme_slug'):
            ctx['programme'] = self.get_programme()
        ctx['back_url'] = get_back_url(self.request)
        ctx['student_searched'] = self.get_student_query()
        ctx['student_total'] = self.student_total
        ctx['qvariable'] = self.query_variable
        return ctx

    def get_student_query(self):
        return self.request.GET.get(self.query_variable)

    def get_programme(self):
        try:
            return Programme.objects.get(slug=self.kwargs['programme_slug'])
        except (Programme.DoesNotExist, KeyError):
            pass

    def get_queryset(self):
        kwargs = {}
        programme__slug = self.kwargs.get('programme_slug')
        if programme__slug:
            kwargs['programme__slug'] = programme__slug
        self.student_total = self.model.objects.filter(**kwargs).count()
        return self.model.objects.get_newly_admitted(query=self.get_student_query(),
                                                     **kwargs)


class StaffAllStudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    permission_required = 'student.list_student'
    template_name = 'student/staff/all.html'
    permission_denied_message = 'You need permission to view student list'
    sortby_kwargs = {
        'profile': 'Name',
        'index_number': 'Index Number',
        'programme': 'Programme',
        'level': 'Level',
        'date_admitted': 'Year Admitted',
        'date_completed': 'Completed',
    }
    sortby_var = 'qsort'
    row_limit_name = 'qlimit'

    def get_context_data(self, *, object_list=None, **kwargs):
        title = 'All Students'
        ctx = super(StaffAllStudentListView, self).get_context_data(object_list=object_list, **kwargs)
        if self.kwargs.get('department_slug'):
            title += ' in \n' + str(self.get_department())
        elif self.kwargs.get('programme_slug'):
            title += ' in \n' + str(self.get_programme())

        ctx['title'] = title
        ctx['header'] = ctx['title']
        ctx['back_url'] = get_back_url(self.request)
        ctx['sort_vars'] = self.sortby_kwargs
        ctx['sortname'] = self.sortby_var
        ctx['current_sort'] = self.get_sort_value()
        ctx['tt_active'] = self.get_only_active()
        ctx['tt_old'] = self.get_active_and_old()
        ctx['student_total'] = ctx['tt_active'] + ctx['tt_old']
        ctx['s_searched'] = self.get_search_query()
        ctx['qty_found'] = self.queryset_counts
        ctx['limit_row'] = self.get_paginate_by_query() or self.paginate_by
        ctx['row_limit_name'] = self.row_limit_name
        return ctx

    def get_active_and_old(self):
        return self.model.objects.get_active_and_old(**self.get_department_programme_kwargs()).count()

    def get_only_active(self):
        return self.model.objects.get_only_active(**self.get_department_programme_kwargs()).count()

    @property
    def paginate_by(self):
        return self.get_paginate_by_query() or 300

    def get_programme(self):
        programme_slug = self.kwargs.get('programme_slug')
        if programme_slug:
            try:
                return Programme.objects.get(
                    slug=programme_slug
                )
            except Programme.DoesNotExist:
                pass

    def get_department(self):
        department_slug = self.kwargs.get('department_slug')
        if department_slug:
            try:
                return Department.objects.get(
                    slug=department_slug
                )
            except Department.DoesNotExist:
                pass

    def get_department_programme_kwargs(self):
        return {
                'department_slug': self.kwargs.get('department_slug'),
                'programme_slug': self.kwargs.get('programme_slug'),
            }

    def get_queryset(self):
        sort_by = self.get_sort_value()
        kwargs = self.get_department_programme_kwargs()
        if sort_by:
            return self.model.objects.get_all_sort(by=sort_by, query=self.get_search_query(), **kwargs)
        queryset = self.model.objects.all(query=self.get_search_query(), **kwargs)
        self.queryset_counts = queryset.count()
        return queryset

    def get_sort_value(self):
        key = self.request.GET.get(self.sortby_var)
        if self.sortby_kwargs.get(key):
            return key

    def get_search_query(self):
        return self.request.GET.get('qstudent')

    def get_paginate_by_query(self):
        return self.request.GET.get('qlimit')


class StudentGroupByDepartment(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Department
    permission_required = 'department.list_department'
    permission_denied_message = 'You need permission to view department list'
    template_name = 'student/staff/selectdepartment.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(StudentGroupByDepartment, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'Select Department'
        ctx['total'] = self.total_department
        ctx['qdepartment'] = self.get_search_query()
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def get_queryset(self):
        return self.model.objects.having_students(name=self.get_search_query())

    def get_search_query(self):
        return self.request.GET.get('qdepartment') or ''

    @property
    def total_department(self):
        return self.model.objects.having_students().count()


class StaffAddPreviousEducation(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # A view for staff to add student previous education usual secondary school to student
    model = StudentPreviousEducation
    template_name = 'student/staff/create.html'
    form_class = StudentPreviousEducationChangeForm
    permission_required = 'student.add_studentpreviouseducation'
    permission_denied_message = 'You need permission to add previous education for student'

    def get_context_data(self, **kwargs):
        ctx = super(StaffAddPreviousEducation, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Previous Education'
        ctx['reuse'] = True
        ctx['header'] = 'School information'
        return ctx

    def get_student(self):
        try:
            return Student.objects.get(
                index_number=self.kwargs['index_number']
            )
        except Student.DoesNotExist:
            raise Http404('The student you want to operate on does not exist in the system')

    def get_form_kwargs(self):
        kwargs = super(StaffAddPreviousEducation, self).get_form_kwargs()
        kwargs['student_id'] = self.get_student().id
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return reverse('Student:staff_register_student', kwargs={
            'index_number': self.get_student().index_number
        })

    def get_object(self, queryset=None):
        obj = self.get_student().get_previous_school()
        if obj:
            return obj
        else:
            return super(StaffAddPreviousEducation, self).get_object(queryset)


class StaffAddStudentForms(LoginRequiredMixin, PermissionRequiredMixin, View):
    # A view for staff to add student admission form to student
    model = StudentForms
    template_name = 'student/staff/create.html'
    permission_required = 'admission.add_studentforms'
    permission_denied_message = 'You need permission to add admission form for student'
    from admission.form import StudentFormsChange
    form_class = StudentFormsChange

    def get_student(self):
        try:
            return Student.objects.get(index_number=self.kwargs['index_number'])
        except Student.DoesNotExist:
            return Http404('The page your looking for can not be found')

    def get_initial(self):
        student_profile = self.get_student().profile
        initial = {'is_current': False, 'candidate_name': student_profile.get_full_name(),
                   'candidate_phone_number': student_profile.phone_number,
                   'sales_agent': self.request.user.get_full_name(),
                   'sales_point_location': student_profile.address.current_region,
                   'sales_point': APP_SETTINGS.INSTITUTION_FULL_NAME,
                   'academic_year': AcademicYear.extract_academic_year(student_profile.student.date_admitted.year)}
        return initial

    def get_object(self):
        try:
            return self.get_student().admission_form
        except ObjectDoesNotExist:
            return

    def get_context_data(self, **kwargs):
        ctx = {'reuse': True, 'title': 'Student Admission Form', 'header': 'Admission Form Details'}
        return ctx

    def get_success_url(self):
        return reverse('Student:staff_register_student', kwargs={'index_number': self.kwargs['index_number']})

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        ctx['form'] = self.form_class(initial=self.get_initial(), instance=self.get_object())
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        form_class = self.form_class(data=self.request.POST, initial=self.get_initial(), instance=self.get_object())
        if form_class.is_valid():
            student = self.get_student()
            admission_instance = form_class.save(False)
            admission_instance.status = FormStatusChoice.ACCEPTED
            admission_instance.save()
            student.admission_form = admission_instance
            student.save()
            return redirect(self.get_success_url())
        ctx['form'] = form_class
        return render(
            request,
            self.template_name,
            ctx
        )


class StaffStudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    template_name = 'student/staff/detail.html'
    permission_required = 'student.staff_view_student'
    permission_denied_message = 'You need permission to view student'

    def get_context_data(self, **kwargs):
        ctx = super(StaffStudentDetailView, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Details'
        ctx['back_url'] = get_back_url(self.request)
        ctx['date_format'] = 'jS E, Y'
        ctx['m_form'] = self.get_password_reset_form()
        return ctx

    def get_password_reset_form(self):
        if not self.object.profile.password and self.request.user.has_perm('accounts.set_password4other'):
            from accounts.forms import SetPasswordForm
            form = SetPasswordForm(self.request.POST or None)
            form.helper.form_action = reverse('Accounts:staff_set_password', kwargs={
                'identity': self.object.profile.identity
            })
            return form
        pass

    def get_object(self, queryset=None):
        return self.model.objects.get(
            profile__identity=self.kwargs['profile__identity'],
            pk=self.kwargs['pk']
        )


class StudentHomePage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'student.view_student'
    template_name = 'student/self/home.html'

    def get_context_data(self, **kwargs):
        student = self.get_student()
        ctx = super(StudentHomePage, self).get_context_data(**kwargs)
        ctx['title'] = f'Student({student}) Home'
        ctx['student'] = student
        return ctx

    def get_student(self):
        try:
            return self.request.user.student
        except ObjectDoesNotExist:
            raise Http404('Your not a student of %s.' % APP_SETTINGS.INSTITUTION_FULL_NAME)

    def get(self, request, *args, **kwargs):
        if not request.user.password:
            return redirect('Accounts:set_pwd')
        return super(StudentHomePage, self).get(request, *args, **kwargs)


class AccountOverviewPage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'student.view_student'
    template_name = 'student/self/accounts/pages/overview.html'

    def get_context_data(self, **kwargs):
        ctx = super(AccountOverviewPage, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Accounts - Overview'
        student = self.get_student()
        ctx['back_url'] = get_back_url(self.request)
        ctx['student'] = student
        ctx['profile'] = student.profile
        ctx['page'] = 'ov'
        return ctx

    def get_student(self):
        return self.request.user.student


class AccountsChangePasswordPage(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'accounts.self_change_password'
    template_name = 'student/self/accounts/updates.html'
    model = User
    form_class = ChangePasswordForm

    def get_context_data(self, **kwargs):
        ctx = super(AccountsChangePasswordPage, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Accounts - Updates'
        ctx['back_url'] = get_back_url(self.request)
        ctx['page'] = 'up'
        ctx['trials'] = 5 - (self.request.session.get('pwd_trial') or 0)
        return ctx

    def form_invalid(self, form):
        returns = super(AccountsChangePasswordPage, self).form_invalid(form)
        pwd_trial = self.request.session.get('pwd_trial')
        if not pwd_trial:
            self.request.session['pwd_trial'] = 1
        elif pwd_trial >= 5:
            self.request.session.clear()
            logout(self.request)
        self.request.session['pwd_trial'] += 1
        return returns

    def form_valid(self, form):
        pwd_trial = self.request.session.get('pwd_trial')
        if not pwd_trial:
            self.request.session['pwd_trial'] = 1
        elif pwd_trial >= 5:
            self.request.session.clear()
            logout(self.request)
        else:
            self.request.session['pwd_trial'] += 1
        return super(AccountsChangePasswordPage, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


class AccountsReportsPage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'student/self/accounts/pages/report.html'
    permission_required = 'student.view_student'

    def get_context_data(self, **kwargs):
        ctx = super(AccountsReportsPage, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Accounts - Report'
        ctx['page'] = 'rp'

        # browser information
        student_profile = self.request.user
        ctx['computer_username'] = student_profile.computer_username
        ctx['computer_name'] = student_profile.computer_name
        ctx['http_sec_ch_ua'] = student_profile.http_sec_ch_ua
        ctx['computer_os'] = student_profile.os
        ctx['last_login'] = student_profile.last_login
        return ctx

    def get_student(self):
        return self.request.user.student


class AccountsProfilePage(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('student.view_student', 'admission.view_own_forms')
    template_name = 'student/self/accounts/pages/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super(AccountsProfilePage, self).get_context_data(**kwargs)
        user = self.request.user
        student = self.request.user.student
        ctx['title'] = 'Student - Accounts - Profile'
        ctx['admission_form'] = student.admission_form
        ctx['student'] = student
        ctx['date_format'] = 'jS E, Y'
        ctx['studentforms'] = student.admission_form
        ctx['profile'] = user
        ctx['address'] = user.address
        ctx['cert_records'] = student.cert_student.certificate_records.all()
        ctx['employment_history'] = user.employment_history
        ctx['sponsor'] = student.student_sponsored
        ctx['programme_choices'] = StudentProgrammeChoice.objects.filter(student_id=student.id).first()
        ctx['previous_education'] = student.previous_education.first()

        return ctx


class AccountsAcademicYearSemester(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'system.can_student_view_semester_and_academic_year'
    permission_denied_message = 'You need permission to access this page'
    from system.models import SemesterAcademicYearModel
    model = SemesterAcademicYearModel
    template_name = 'student/self/accounts/pages/semesterAcademic.html'

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(is_current=True)
        except self.model.DoesNotExist:
            raise Http404('Please try again later')

    def get_context_data(self, **kwargs):
        ctx = super(AccountsAcademicYearSemester, self).get_context_data(**kwargs)
        ctx['title'] = 'Semester and Academic Year'
        return ctx


class AccountsPermissions(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'student/self/accounts/pages/permissions.html'
    permission_denied_message = 'You need permission to view this page'

    def get_context_data(self, **kwargs):
        ctx = super(AccountsPermissions, self).get_context_data(**kwargs)
        ctx['title'] = 'Permissions Group'
        return ctx

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


from django.views.generic import TemplateView, ListView, DetailView,  CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.response import HttpResponseForbidden
from django.utils.timezone import now as today_time
from system.models import Level


from .generate_serial_number import SerialNumberGenerator
from .models import (
    FormTypeChoicesModel,
    StudentForms,
    FormStatusChoice,
    models,
)
from student.models import (
    AdmissionCertificate,
    CertExamRecord,
    StudentProgrammeChoice,
    StudentPreviousEducation,
)
from empoymentHistory.models import EmploymentHistoryModel
from sponsor.models import StudentSponsor
from .form import (
    AdmissionLoginForm,
    StudentFormsCreation,
    StudentFormsChange,
    AdmissionFromBatchCreation,
    FormTypeChoicesModelCreationForm,
    AcceptanceConfirmationForm
)

from CollegeManagementSystem.settings import INSTITUTION_FULL_NAME


def get_academic_year():
    import datetime
    to_year = datetime.date.today().year
    return to_year - 1, to_year


class AdmissionFormCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'admission/admin/create.html'
    permission_required = 'admission.add_studentforms'
    model = StudentForms
    form_class = StudentFormsCreation

    def get_context_data(self, **kwargs):
        ctx = super(AdmissionFormCreateView, self).get_context_data(**kwargs)
        ctx['header'] = 'Add Admission Form'
        ctx['title'] = 'Add Admission Form'
        return ctx


class AdmissionFormChangeView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'admission/admin/create.html'
    permission_required = ('admission.change_studentforms',  'admission.view_studentforms', )
    model = StudentForms
    form_class = StudentFormsChange

    def get_context_data(self, **kwargs):
        ctx = super(AdmissionFormChangeView, self).get_context_data(**kwargs)
        ctx['header'] = 'Change Admission Form'
        ctx['title'] = 'Change Admission Form'
        ctx['back_url'] = self.request.GET.get('back')
        return ctx

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, serial_number=self.kwargs['serial_number'], id=self.kwargs['id'])


class AdmissionMainTemplateView(TemplateView):
    template_name = 'admission/main_template_view.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdmissionMainTemplateView, self).get_context_data(**kwargs)
        ctx["title"] = 'Admission'
        ctx['admission_forms_types'] = self.get_student_admission_types()
        ctx["academic_year"] = get_academic_year()
        return ctx

    def get_student_admission_types(self):
        return FormTypeChoicesModel.objects.all()


class StudentFormLoginTemplateView(TemplateView):
    template_name = 'forms/login.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = 'admission login'
        ctx["form_type"] = self.get_form_type()
        ctx["form"] = AdmissionLoginForm()
        return ctx

    def get_form_type(self):
        return get_object_or_404(FormTypeChoicesModel, id=self.kwargs["formtypeid"])

    def post(self, request, *args, **kwargs):
        admission_login_form = AdmissionLoginForm(request.POST)
        if admission_login_form.is_valid():
            serial_number = admission_login_form.cleaned_data['serial_number']
            pin_code = admission_login_form.cleaned_data['pin_code']
            try:
                admission_form = StudentForms.objects.get(serial_number=serial_number, pin_code=pin_code)
                if admission_form.status == FormStatusChoice.EXPIRED:
                    admission_login_form.add_error('serial_number', 'this form has expired')
                    pass
                elif admission_form.status == FormStatusChoice.COMPLETED:
                    pass

            except StudentForms.DoesNotExist:
                admission_login_form.add_error('serial_number', 'Enter a correct "SERIAL NUMBER" on the form')
                admission_login_form.add_error('pin_code', 'Enter a correct "PIN CODE" on the form')
            else:
                return redirect('Student:admission-redirect', serial_number=serial_number)
        ctx = self.get_context_data()
        ctx['form'] = admission_login_form
        return render(request, context=ctx, template_name=self.template_name)


class AdmissionAdministrationTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'admission/admin/main_page.html'
    permission_required = 'admission.view_studentforms'

    def get_context_data(self, **kwargs):
        ctx = super(AdmissionAdministrationTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Admission'
        ctx['can_audit'] = self.can_audit()
        return ctx

    def get_admission_form_groups(self):
        return

    def can_audit(self):
        return self.request.user.is_staff


class AllAdmissionFormsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'admission/admin/list.html'
    permission_required = 'admission.view_studentforms'
    model = StudentForms
    paginate_by = 200

    def get_context_data(self, **kwargs):
        ctx = super(AllAdmissionFormsListView, self).get_context_data(**kwargs)
        ctx['title'] = 'All Admission Forms'
        ctx['all_objs'] = self.model.objects.count()
        ctx['form_status'] = FormStatusChoice
        ctx['empty_text'] = self.get_empty_text()
        ctx['query_text'] = self.get_querytext()
        ctx['fQuery'] = self.get_filter_query()
        return ctx

    def get_empty_text(self):
        query_text = self.get_querytext()
        if query_text:
            return '"%s" matches no student admission form' % query_text
        status = self.get_filter_query()
        if status:
            return 'There is no student admission form with "%s" status' % status
        return 'No students has applied yet'

    def get_querytext(self):
        return self.request.GET.get('studentforms') or ''

    def get_queryset(self):
        return self.model.objects.search(self.get_querytext(), status=self.get_filter_query())

    def get_filter_query(self):
        return self.request.GET.get('fQuery')


class StudentFormsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'admission.view_studentforms'
    template_name = 'admission/admin/detail.html'
    permission_denied_message = 'You need permission to view student forms'
    model = StudentForms
    acceptance_form = AcceptanceConfirmationForm

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def get_context_data(self, **kwargs):
        ctx = super(StudentFormsDetailView, self).get_context_data(**kwargs)
        ctx['title'] = '%s' % self.object
        ctx['back_url'] = self.get_back_url()
        ctx['back_name'] = self.get_back_name()
        ctx['cert_records'] = self.get_all_cert_records()
        ctx['certificate'] = self.certificate_object
        ctx['employment_history'] = self.get_student_employment_history()
        ctx['sponsor'] = self.get_student_sponsor()
        ctx['programme_choices'] = self.get_programme_choices()
        ctx['previous_education'] = self.get_student_previous_education()
        ctx['can_audit_form'] = self.can_user_audit_forms()
        ctx['acceptance_form'] = self.acceptance_form(self.request.POST or None, instance=self.get_programme_choices())
        return ctx

    def get_student_employment_history(self):
        return EmploymentHistoryModel.objects.filter(
            employee_id=self.object.student.profile_id
        ).first()

    def get_student_sponsor(self):
        return StudentSponsor.objects.filter(
            student_id=self.object.student.id
        ).first()

    def get_programme_choices(self):
        return StudentProgrammeChoice.objects.filter(
            student_id=self.object.student.id
        ).first()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        acceptance_form = self.acceptance_form(request.POST, instance=self.get_programme_choices())
        if acceptance_form.is_valid():
            programme_given = acceptance_form.cleaned_data['Select_programme_for_student']
            student = self.object.student
            student.programme_id = programme_given
            student.date_admitted = today_time().date()
            student.level = Level.objects.get_4first_year()
            student.save()
            admission_form = self.object
            admission_form.status = FormStatusChoice.ACCEPTED
            admission_form.save()
            return redirect('Admission:accept_form', serial_number=admission_form.serial_number, id=admission_form.id)
        return self.get(request, *args, **kwargs)

    def get_back_url(self):
        return self.request.GET.get('back') or reverse('Admission:allforms')

    def get_back_name(self):
        return self.request.GET.get('backname') or 'forms'

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            serial_number=self.kwargs['serial_number'],
            id=self.kwargs['id'],
        )

    def get_student_certificate(self):
        try:
            student_id = self.object.student.id
        except models.ObjectDoesNotExist:
            pass
        else:
            return AdmissionCertificate.objects.filter(
                student_id=student_id
            ).first()

    def get_student_previous_education(self):
        return StudentPreviousEducation.objects.filter(
            student_id=self.object.student.id
        ).first()

    def get_all_cert_records(self):
        self.certificate_object = self.get_student_certificate()
        return CertExamRecord.objects.get_for_certificate(self.certificate_object.id)

    def can_user_audit_forms(self):
        return not self.object.is_locked and self.request.user.has_perm('admission.can_audit_admission_form')


class StudentFormsPrintView(TemplateView, LoginRequiredMixin):
    template_name = 'admission/student/printAdmissionForm.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        self.student = user.student
        if self.student:
            return super(StudentFormsPrintView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden

    def get_context_data(self, **kwargs):
        ctx = super(StudentFormsPrintView, self).get_context_data(**kwargs)
        ctx['student'] = self.student
        ctx['title'] = 'Print Admission Form'
        ctx['subtitle'] = 'Print Admission Forms'
        ctx['profile'] = self.get_profile()
        ctx['admission_form'] = self.get_admission_form()
        ctx['institution_name'] = INSTITUTION_FULL_NAME
        ctx['address'] = self.get_address()
        ctx['certificate'] = self.get_certificate()
        ctx['employment_history'] = self.get_employment_history()
        ctx['sponsor'] = self.get_sponsor()
        ctx['previous_education'] = self.get_previous_education()
        ctx['programme_choices'] = self.get_programme_choices()
        return ctx

    def get_profile(self):
        return self.student.profile

    def get_admission_form(self):
        return self.student.admission_form

    def get_address(self):
        return self.student.profile.address

    def get_certificate(self):
        return self.student.cert_student.certificate_records.all()

    def get_employment_history(self):
        try:
            employment_his = EmploymentHistoryModel.objects.get(employee=self.request.user)
        except employment_his.DoesNotExist:
            pass

    def get_sponsor(self):
        return self.student.student_sponsored

    def get_previous_education(self):
        return StudentPreviousEducation.objects.get(student=self.student)

    def get_programme_choices(self):
        return self.student.programme_choices


class StudentFormSubmitView(TemplateView, LoginRequiredMixin):
    template_name = 'admission/student/submitForms.html'

    def get_login_url(self):
        return reverse('Admission:login')

    def get_context_data(self, **kwargs):
        ctx = super(StudentFormSubmitView, self).get_context_data(**kwargs)
        ctx['subtitle'] = 'FORM SUBMITTED ✔️'
        ctx['title'] = 'form submission'
        admission_form = self.student.admission_form
        if admission_form.status != FormStatusChoice.SUBMITTED:
            admission_form.status = FormStatusChoice.SUBMITTED
            admission_form.save()
            ctx['submitted'] = True
        ctx['admission_form'] = admission_form
        return ctx

    def get(self, request, *args, **kwargs):
        user = request.user
        self.student = user.student
        if self.student:
            admission_form = self.student.admission_form
            if admission_form.status in (
                    FormStatusChoice.REJECTED,
                    FormStatusChoice.ACCEPTED,
                    FormStatusChoice.EXPIRED,
            ):
                return redirect('Institution:admission_error')
            else:
                return super(StudentFormSubmitView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden


class StudentFormsAcceptView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'admission.can_accept_studentform'
    template_name = 'admission/staff/accept.html'
    model = StudentForms

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            serial_number=self.kwargs['serial_number'],
            id=self.kwargs['id']
        )

    def get_context_data(self, **kwargs):
        ctx = super(StudentFormsAcceptView, self).get_context_data(**kwargs)
        ctx['title'] = 'reject admission form'
        ctx['back_url'] = self.request.GET.get('back') or reverse('Admission:form_details',
                                                                  kwargs={
                                                                      'serial_number': self.object.serial_number,
                                                                      'id': self.object.id
                                                                  })
        ctx['student'] = self.get_student()
        return ctx

    def get_student(self):
        return self.object.student


class AdmissionFormDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'admission.view_studentform_detail'
    model = StudentForms
    template_name = 'admission/staff/admission_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            serial_number=self.kwargs['serial_number']
        )

    def get_context_data(self, **kwargs):
        ctx = super(AdmissionFormDetailView, self).get_context_data(**kwargs)
        ctx['title'] = '%s Detail' % self.object
        return ctx


class AdmissionCreateBatchFormsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = StudentForms
    template_name = 'admission/staff/create_batch.html'
    form_class = AdmissionFromBatchCreation
    permission_required = 'admission.add_studentforms'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Admission Batch Creation',
            'wrap2flex': True
        }

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        ctx['form'] = self.form_class()
        return render(
            request, self.template_name, ctx
        )

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        form_class = self.form_class(request.POST)
        if form_class.is_valid():
            prefix = form_class.cleaned_data.get('prefix')
            suffix = form_class.cleaned_data.get('suffix')
            form_type = form_class.cleaned_data['form_type']
            cost = form_class.cleaned_data.get('cost')
            qty = form_class.cleaned_data['quantity']
            academic_year = form_class.cleaned_data['academic_year']
            pin_code_length = form_class.cleaned_data.get('pin_code_length')
            serial_number_generator = SerialNumberGenerator(prefix=prefix, suffix=suffix, quantity=qty, pin_code_len=pin_code_length)
            objects_created = self.model.objects.bulk_create(
                objs=[self.model(serial_number=sn, academic_year=academic_year, cost=cost, form_type=form_type, pin_code=serial_number_generator.pin_code()) for sn in serial_number_generator]
            )
            if objects_created:
                request.session['admission_objs_created'] = ','.join(sn.serial_number for sn in objects_created)
                return redirect('Admission:batch_job_result')

        ctx['form'] = form_class
        return render(
            request, self.template_name, ctx
        )


class AdmissionBatchCreatedView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StudentForms
    template_name = 'admission/staff/listBatchNowCreated.html'
    permission_required = 'admission.view_studentforms'

    def get_queryset(self):
        queryset = self.model.objects.filter(
            serial_number__in=self.admission_objs_created
        )
        self.num_objs_created = queryset.count()
        return queryset

    def get(self, request, *args, **kwargs):
        admission_objs_created = self.request.session.get('admission_objs_created')
        if admission_objs_created:
            self.admission_objs_created = str(admission_objs_created).split(',')
            del self.request.session['admission_objs_created']
            return super(AdmissionBatchCreatedView, self).get(request, *args, **kwargs)
        return redirect('Admission:allforms')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(AdmissionBatchCreatedView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'admission batch job'
        ctx['num_objs_created'] = self.num_objs_created
        return ctx


class FormTypeModelListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'admission.view_formtypechoicesmodel'
    model = FormTypeChoicesModel
    template_name = 'admission/formtype/list.html'
    search_name = 'formtype'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(FormTypeModelListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'Form Type'
        ctx['tt_category'] = self.get_total_formtypes()
        ctx['tt_result'] = self.object_list.count()
        ctx['has_add_perm'] = self.can_user_add_formtype()
        ctx['can_delete'] = self.can_user_delete_formtype()
        ctx['search_name'] = self.search_name
        ctx['search_value'] = self.request.GET.get(self.search_name)
        return ctx

    def get_total_formtypes(self):
        return self.model.objects.count()

    def get_queryset(self):
        return self.model.objects.search(self.request.GET.get(self.search_name))

    def can_user_add_formtype(self):
        return self.request.user.has_perm('add_formtypechoicesmodel')

    def can_user_delete_formtype(self):
        return self.request.user.has_perm('delete_formtypechoicesmodel')


class FormTypeModelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'admission.add_formtypechoicesmodel'
    model = FormTypeChoicesModel
    template_name = 'admission/formtype/create.html'
    form_class = FormTypeChoicesModelCreationForm

    def get_context_data(self, **kwargs):
        ctx = super(FormTypeModelCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Form Type'
        ctx['header'] = 'Add Form Type'
        ctx['back_url'] = self.request.GET.get('back')
        return ctx


class FormTypeModelChangeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'admission.change_formtypechoicesmodel'
    model = FormTypeChoicesModel
    template_name = 'admission/formtype/create.html'
    form_class = FormTypeChoicesModelCreationForm

    def get_context_data(self, **kwargs):
        ctx = super(FormTypeModelChangeView, self).get_context_data(**kwargs)
        ctx['title'] = 'Edit Form Type'
        ctx['header'] = 'Edit %s' % self.object
        ctx['back_url'] = self.request.GET.get('back')
        return ctx

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            title=self.kwargs['title'],
            id=self.kwargs['id'],
        )


class FormTypeModeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'admission.view_formtypechoicesmodel'
    model = FormTypeChoicesModel
    template_name = 'admission/formtype/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            title=self.kwargs['title'],
            id=self.kwargs['id'],
        )

    def get_context_data(self, **kwargs):
        ctx = super(FormTypeModeDetailView, self).get_context_data(**kwargs)
        ctx['title'] = '%s Detail' % self.object
        ctx['back_url'] = self.request.GET.get('back') or reverse('Admission:form_type_list')
        return ctx


class HandleAdmissionExceptions(LoginRequiredMixin, TemplateView):
    template_name = 'admission/student/exception.html'

    def get_login_url(self):
        return reverse('Admission:main_template_page')

    def get_context_data(self, **kwargs):
        ctx = super(HandleAdmissionExceptions, self).get_context_data(**kwargs)
        ctx['title'] = 'Admission Exception'
        ctx['admission_form'] = self.get_admission_form()

        return ctx

    def get_admission_form(self):
        return get_object_or_404(StudentForms, serial_number=self.request.user.identity)

# TODO create grading algorithm to auto grade student and picked student and auto assigned programme
# TODO create admission for on purchase. Only generate admission form on purchase for a particular programme

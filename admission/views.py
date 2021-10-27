from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect, render

from .models import FormTypeChoicesModel, StudentForms, FormStatusChoice
from .form import AdmissionLoginForm


def get_academic_year():
    import datetime
    to_year = datetime.date.today().year
    return to_year - 1, to_year


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
                if admission_form.status == FormStatusChoice.Expired:
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

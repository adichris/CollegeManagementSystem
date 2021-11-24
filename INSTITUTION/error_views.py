from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from admission.models import FormStatusChoice


class AdmissionErrorTemplateView(TemplateView, LoginRequiredMixin):
    template_name = 'institution/errors/admissionError.html'

    def get_login_url(self):
        return reverse('Admission:login')

    def get_context_data(self, **kwargs):
        ctx = super(AdmissionErrorTemplateView, self).get_context_data(**kwargs)
        admissionF_status = self.request.user.student.admission_form.status
        if admissionF_status == FormStatusChoice.EXPIRED:
            err_header = 'Admission Forms is Expired'
            err_passage = 'Your admission form is not application.\n We can not process your forms' \
                          ' as this admission forms has expire and hence seized application.' \
                          '\nBuy a new admission forms and start applying'
        elif admissionF_status == FormStatusChoice.ACCEPTED:
            err_header = 'Admission Forms Accepted'
            err_passage = 'Your Forms has been accepted by the institution {INSTITUTION_FULL_NAME}.\n' \
                          'You can start the necessary preparations'
        elif admissionF_status == FormStatusChoice.REJECTED:
            err_header = 'Your Forms Has Been Rejected'
            err_passage = 'Please start over with an new admission form'
        else:
            err_header = 'Not Applicable'
            err_passage = 'We have encountered an error in your admission form form'

        ctx['title'] = 'Admission Error'
        ctx['subtitle'] = err_header
        ctx['errPassage'] = err_passage
        ctx['form_status'] = FormStatusChoice
        ctx['admissionF_status'] = self.request.user.student.admission_form.status
        return ctx

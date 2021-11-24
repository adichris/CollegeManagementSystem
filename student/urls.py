from django.urls import path

from .views import (
    StudentAdmissionRedirectView,
    StudentProgrammeSelectionView,
    AdmissionCertificateExaminationView,
    StudentPreviousEducationChangeView,
    StudentAdmissionDetails
)

app_name = 'Student'
urlpatterns = [
    path('admissionredirect/<str:serial_number>', StudentAdmissionRedirectView.as_view(),
         name='admission-redirect'),
    path('programmechoices/', StudentProgrammeSelectionView.as_view(), name='programmes_choices'),
    path('admissioncertificateexamsrecords/', AdmissionCertificateExaminationView.as_view(), name='admission_cert_exam_records'),
    path('studentpreviouseducation/', StudentPreviousEducationChangeView.as_view(), name='admission_previous_education'),
    path('admission/details/', StudentAdmissionDetails.as_view(), name='admission_detail')
]

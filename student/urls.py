from django.urls import path, include

from .views import (
    StudentAdmissionRedirectView,
    StudentProgrammeSelectionView,
    AdmissionCertificateExaminationView,
    StudentPreviousEducationChangeView,
    StudentAdmissionDetails,
    StaffStudentTemplateView,
    StaffRegisterStudentDetailView,
    StaffStudentCreateView,
    StaffStudentUpdateIndexNumProgrammeUpdateView,
)

app_name = 'Student'

staff_urlpatterns = [
    path('', StaffStudentTemplateView.as_view(), name='staff_home'),
    path('add/', StaffStudentCreateView.as_view(), name='staff_register'),
    path('changeindexnumberandprogramme/<str:index_number>/', StaffStudentUpdateIndexNumProgrammeUpdateView.as_view(),
         name='staff_change_indexPrg'),
    path('add/continuous/<str:index_number>/', StaffRegisterStudentDetailView.as_view(), name='staff_register_student'),
    path('add/certificate/<str:index_number>/', AdmissionCertificateExaminationView.as_view(), name='staff_add_cert'),

]

urlpatterns = [
    path('staff/', include(staff_urlpatterns)),
    path('admissionredirect/<str:serial_number>', StudentAdmissionRedirectView.as_view(),
         name='admission-redirect'),
    path('programmechoices/', StudentProgrammeSelectionView.as_view(), name='programmes_choices'),
    path('admissioncertificateexamsrecords/', AdmissionCertificateExaminationView.as_view(), name='admission_cert_exam_records'),
    path('studentpreviouseducation/', StudentPreviousEducationChangeView.as_view(), name='admission_previous_education'),
    path('admission/details/', StudentAdmissionDetails.as_view(), name='admission_detail')
]

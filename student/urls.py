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
    NewlyAdmittedStudentListView,
    StaffSelectStudentProgramme,
    StaffAllStudentListView,
    StudentGroupByDepartment,
    StaffAddPreviousEducation,
    StaffAddStudentForms,
)

app_name = 'Student'

staff_urlpatterns = [
    path('', StaffStudentTemplateView.as_view(), name='staff_home'),
    path('add/', StaffStudentCreateView.as_view(), name='staff_register'),
    path('changeindexnumberandprogramme/<str:index_number>/', StaffStudentUpdateIndexNumProgrammeUpdateView.as_view(),
         name='staff_change_indexPrg'),
    path('add/continuous/<str:index_number>/', StaffRegisterStudentDetailView.as_view(), name='staff_register_student'),
    path('add/certificate/<str:index_number>/', AdmissionCertificateExaminationView.as_view(), name='staff_add_cert'),
    path('newly/admitted/<slug:programme_slug>/', NewlyAdmittedStudentListView.as_view(), name='staff_newly_admitted'),
    path('newly/admitted/', NewlyAdmittedStudentListView.as_view(), name='staff_newly_admitted_search'),
    path('selectgroupbyprogramme/newlyadmitted', StaffSelectStudentProgramme.as_view(), name='staff_select_student_programme'),
    path('all/', StaffAllStudentListView.as_view(), name='staff_all'),
    path('alldepartment/<slug:department_slug>/', StaffAllStudentListView.as_view(), name='staff_department_all'),
    path('allprogramme/<slug:programme_slug>/', StaffAllStudentListView.as_view(), name='staff_programme_all'),
    path('group/department/', StudentGroupByDepartment.as_view(), name='department_group'),
    path('programmechoices/<str:index_number>/', StudentProgrammeSelectionView.as_view(), name='staff_add_programmes_choices'),
    path('addpreviuoseducation/<str:index_number>/', StaffAddPreviousEducation.as_view(), name='staff_add_previouseducation'),
    path('addadmissionform/<str:index_number>/', StaffAddStudentForms.as_view(), name='staff_add_admissionform'),
]

urlpatterns = [
    path('staff/', include(staff_urlpatterns)),
    path('admissionredirect/<str:serial_number>', StudentAdmissionRedirectView.as_view(),
         name='admission-redirect'),
    path('programmechoices/', StudentProgrammeSelectionView.as_view(), name='programmes_choices'),
    path('admissioncertificateexamsrecords/', AdmissionCertificateExaminationView.as_view(), name='admission_cert_exam_records'),
    path('studentpreviouseducation/', StudentPreviousEducationChangeView.as_view(), name='admission_previous_education'),
    path('admission/details/', StudentAdmissionDetails.as_view(), name='admission_detail'),
]

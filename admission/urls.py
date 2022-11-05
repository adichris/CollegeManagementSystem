from django.urls import path, include

from .views import (
    AdmissionMainTemplateView,
    StudentFormLoginTemplateView,
    AdmissionAdministrationTemplateView,
    AllAdmissionFormsListView,
    StudentFormsDetailView,
    StudentFormsAcceptView,
    StudentFormsPrintView,
    StudentFormSubmitView,
    AdmissionFormCreateView,
    AdmissionFormDetailView,
    AdmissionFormChangeView,
    AdmissionCreateBatchFormsView,
    AdmissionBatchCreatedView,
    FormTypeModelCreateView,
    FormTypeModelListView,
    FormTypeModeDetailView,
    FormTypeModelChangeView,
    HandleAdmissionExceptions,
    FormTypeModelDelete,
)


app_name = 'Admission'
student_admission_urlpatterns = [
    path('', AdmissionMainTemplateView.as_view(), name='main_template_page'),
    path('login/<int:formtypeid>/', StudentFormLoginTemplateView.as_view(), name='login'),
    path('printforms/', StudentFormsPrintView.as_view(), name='stu_print_form'),
    path('submitforms/', StudentFormSubmitView.as_view(), name='stu_submit_form'),
    path('exceptionhandle/', HandleAdmissionExceptions.as_view(), name='handle_exceptions'),
]

staff_urlpatterns = [
    path('allforms/', AllAdmissionFormsListView.as_view(), name='allforms'),
    path('', AdmissionAdministrationTemplateView.as_view(), name='admins'),
    path('add/', AdmissionFormCreateView.as_view(), name='create'),
    path('change/<str:serial_number>/<int:id>/', AdmissionFormChangeView.as_view(), name='change'),
    path('formsdetails/<str:serial_number>/<int:id>/', StudentFormsDetailView.as_view(), name='form_details'),
    path('acceptform/<str:serial_number>/<int:id>/', StudentFormsAcceptView.as_view(), name='accept_form'),
    path('detail/<str:serial_number>/', AdmissionFormDetailView.as_view(), name='detail'),
    path('generatebatch/', AdmissionCreateBatchFormsView.as_view(), name='create_batch'),
    path('generatebatch/completed/', AdmissionBatchCreatedView.as_view(), name='batch_job_result'),
    path('formtype/add/', FormTypeModelCreateView.as_view(), name='form_type_create'),
    path('formtype/list/', FormTypeModelListView.as_view(), name='form_type_list'),
    path('formtype/detail/<str:title>/<int:id>', FormTypeModeDetailView.as_view(), name='form_type_detail'),
    path('formtype/change/<str:title>/<int:id>', FormTypeModelChangeView.as_view(), name='form_type_update'),
    path('formtypedelete/<str:title>/<pk>/', FormTypeModelDelete.as_view(), name="form_type_delete"),
]

urlpatterns = [
    path('', include(student_admission_urlpatterns)),
    path('staff/', include(staff_urlpatterns)),
]

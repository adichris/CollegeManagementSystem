from django.urls import path, include

from .views import (
    StudentProfileCreateView,
    ContinuouStudentProfileCreateView,
    LecturerProfileCreateView,
    SetPassword4other
)

app_name = 'Accounts'

urlpatternsAjax = [
    path('staffsetpassword/<str:identity>/', SetPassword4other.as_view(), name='staff_set_password')
]

urlpatterns = [
    path('studentadmission/profile/<str:serial_number>/',
         StudentProfileCreateView.as_view(), name='admission_student_profile'),
    path('add/student/profile/<str:index_number>/',
         ContinuouStudentProfileCreateView.as_view(), name='create_student_profile'),
    path('add/lecturer/<str:identity>/', LecturerProfileCreateView.as_view(), name='create_lecturer'),
    path('ajax/', include(urlpatternsAjax))
]

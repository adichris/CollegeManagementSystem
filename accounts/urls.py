from django.urls import path

from .views import (
    StudentProfileCreateView,
    ContinuouStudentProfileCreateView,
)

app_name = 'Accounts'
urlpatterns = [
    path('studentadmission/profile/<str:serial_number>/',
         StudentProfileCreateView.as_view(), name='admission_student_profile'),
    path('add/student/profile/<str:index_number>/',
         ContinuouStudentProfileCreateView.as_view(), name='create_student_profile'),
]

from django.urls import path

from .views import StudentProfileCreateView

app_name = 'Accounts'
urlpatterns = [
    path('studentadmission/profile/<str:serial_number>/', StudentProfileCreateView.as_view(), name='admission_student_profile')
]

from django.urls import path

from .views import (
    StudentSponsorCreateView,
    StaffSponsorCreateView,
)

app_name = 'Sponsor'
urlpatterns = [
    path('student/admission/', StudentSponsorCreateView.as_view(), name='student_admission'),
    path('staff/create/<str:index_number>/', StaffSponsorCreateView.as_view(), name='staff_create'),
]

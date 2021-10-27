from django.urls import path

from .views import StudentSponsorCreateView

app_name = 'Sponsor'
urlpatterns = [
    path('student/admission/', StudentSponsorCreateView.as_view(), name='student_admission'),
]

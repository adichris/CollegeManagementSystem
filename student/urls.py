from django.urls import path

from .views import StudentAdmissionRedirectView

app_name = 'Student'
urlpatterns = [
    path('admissionredirect/<str:serial_number>', StudentAdmissionRedirectView.as_view(),
         name='admission-redirect'),
]

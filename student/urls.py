from django.urls import path

from .views import (
    StudentAdmissionRedirectView,
    StudentProgrammeSelectionView,
)

app_name = 'Student'
urlpatterns = [
    path('admissionredirect/<str:serial_number>', StudentAdmissionRedirectView.as_view(),
         name='admission-redirect'),
    path('programmechoices/', StudentProgrammeSelectionView.as_view(), name='programmes_choices')
]

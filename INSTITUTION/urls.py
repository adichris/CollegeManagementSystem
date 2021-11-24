from django.urls import path

from .error_views import (
    AdmissionErrorTemplateView,
)

app_name = 'Institution'
urlpatterns = [
    path('admissionError/', AdmissionErrorTemplateView.as_view(), name='admission_error'),

]

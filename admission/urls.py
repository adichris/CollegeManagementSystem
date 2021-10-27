from django.urls import path
from .views import AdmissionMainTemplateView, StudentFormLoginTemplateView

app_name = 'Admission'
urlpatterns = [
    path('', AdmissionMainTemplateView.as_view(), name='main_template_page'),
    path('login/<int:formtypeid>/', StudentFormLoginTemplateView.as_view(), name='login'),
]

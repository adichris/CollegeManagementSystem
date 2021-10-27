from django.urls import path
from .views import StudentAddressCreateView


app_name = 'Address'
urlpatterns = [
    path('studentaddress/create/', StudentAddressCreateView.as_view(), name='admission_student_create'),
]

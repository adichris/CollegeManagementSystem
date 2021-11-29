from django.urls import path
from .views import (
    StudentAddressCreateView,
    UserAddressCreateView,
)


app_name = 'Address'
urlpatterns = [
    path('studentaddress/create/', StudentAddressCreateView.as_view(), name='admission_student_create'),
    path('staff/create/<str:profile_slug>/', UserAddressCreateView.as_view(), name='staff_student_create'),
]

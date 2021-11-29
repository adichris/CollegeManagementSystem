from django.urls import path, include

from .views import (
    StaffLecturerTemplateView,
)

app_name = 'Lecturer'

staff_urlpatterns = [
    path('', StaffLecturerTemplateView.as_view(), name='staff_template')
]

urlpatterns = [
    path('staff/', include(staff_urlpatterns)),
]

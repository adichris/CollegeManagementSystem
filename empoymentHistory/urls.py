from django.urls import path
from .views import (
    EmploymentHistoryCreateUpdateView,
    UserEmploymentHistoryCreateView
)


app_name = 'EmploymentHistory'
urlpatterns = [
    path('admission/student/employmentHistory/', EmploymentHistoryCreateUpdateView.as_view(),
         name='student_admission_create_history'),
    path('staff/create/<slug:profile_slug>/', UserEmploymentHistoryCreateView.as_view(),
         name='staff_create'),

]

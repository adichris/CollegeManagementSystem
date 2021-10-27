from django.urls import path
from .views import EmploymentHistoryCreateUpdateView


app_name = 'EmploymentHistory'
urlpatterns = [
    path('admission/student/employmentHistory/', EmploymentHistoryCreateUpdateView.as_view(),
         name='student_admission_create_history'),
]

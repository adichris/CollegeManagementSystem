from django.urls import path, include
from .views import (
    EmploymentHistoryCreateUpdateView,
    UserEmploymentHistoryCreateView,
    get_employment_history_ajax,
)


app_name = 'EmploymentHistory'

ajax_urlpatterns = [
    path('uremploymenthistory/<slug:profile_slug>', get_employment_history_ajax, name='old_employment_history')
]
urlpatterns = [
    path('admission/student/employmentHistory/', EmploymentHistoryCreateUpdateView.as_view(),
         name='student_admission_create_history'),
    path('staff/create/<slug:profile_slug>/', UserEmploymentHistoryCreateView.as_view(),
         name='staff_create'),
    path('ajax/', include(ajax_urlpatterns)),
]

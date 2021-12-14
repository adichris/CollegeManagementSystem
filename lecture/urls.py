from django.urls import path, include

from .views import (
    StaffLecturerTemplateView,
    AddLecturerView,
    AddLecturerTemplateView,
    LecturerApplicationCreateView,
    LecturerDepartmentAssignment,
    LecturerListView,
)

app_name = 'Lecturer'

staff_urlpatterns = [
    path('', StaffLecturerTemplateView.as_view(), name='staff_template'),
    path('add/', AddLecturerView.as_view(), name='staff_add'),
    path('addhome/<str:identity>/', AddLecturerTemplateView.as_view(), name='staff_add_template'),
    path('applicationform/<str:identity>/', LecturerApplicationCreateView.as_view(), name='staff_app_change'),
    path('assigndepartment/<str:identity>/', LecturerDepartmentAssignment.as_view(), name='staff_assign_department'),
    path('all/', LecturerListView.as_view(), name='staff_all'),
    path('all/<slug:department_slug>/', LecturerListView.as_view(), name='staff_department_all'),
]

urlpatterns = [
    path('staff/', include(staff_urlpatterns)),
]

from django.urls import path
from .views import (
    SemesterCreateView,
    SemesterAcademicYearView,
    SemesterUpdateView,
    PermissionGroupListView,
)


app_name = 'System'
urlpatterns = [
    path('semester/new/', SemesterCreateView.as_view(), name='semester_new'),
    path('semester/change/<str:name>/<int:id>/', SemesterUpdateView.as_view(), name='semester_update'),
    path('semesteracademicyear/', SemesterAcademicYearView.as_view(), name='semester_academic_year'),
    path('permissiongroups/', PermissionGroupListView.as_view(), name='permission_group'),
]

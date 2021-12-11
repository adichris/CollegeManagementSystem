from django.urls import path
from .views import (
    SemesterCreateView,
    SemesterAcademicYearView,
    SemesterUpdateView,
    PermissionGroupListView,
    PermissionGroupCreate,
    PermissionGroupDetails,
    PermissionDetail
)


app_name = 'System'
urlpatterns = [
    path('semester/new/', SemesterCreateView.as_view(), name='semester_new'),
    path('semester/change/<str:name>/<int:id>/', SemesterUpdateView.as_view(), name='semester_update'),
    path('semesteracademicyear/', SemesterAcademicYearView.as_view(), name='semester_academic_year'),
    path('permissiongroups/', PermissionGroupListView.as_view(), name='permission_group'),
    path('permissiongroup/add/', PermissionGroupCreate.as_view(), name='permission_group_add'),
    path('permissiongroup/<int:pk>/', PermissionGroupDetails.as_view(), name='permission_group_detail'),
    path('permissiondetail/<int:permission_pk>/', PermissionDetail.as_view(), name='permission_detail'),
]

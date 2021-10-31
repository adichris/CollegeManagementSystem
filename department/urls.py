from django.urls import path, include

from .views import (
    DepartmentsListView,
    DepartmentCreateView,
    DepartmentDetailView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    FacultyDepartmentListView
)


app_name = 'Department'
department_urlpatterns = [
    path('all/', DepartmentsListView.as_view(), name='list'),
    path('add/', DepartmentCreateView.as_view(), name='create'),
    path('<slug:slug>/', DepartmentDetailView.as_view(), name='detail'),
    path('change/<slug:slug>/', DepartmentUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', DepartmentDeleteView.as_view(), name='delete'),
    path('inthisfaculty/<slug:faculty_slug>/', FacultyDepartmentListView.as_view(), name='4faculty')
]


urlpatterns = [
    path('', include(department_urlpatterns)),
    path('programme/', include('programme.urls')),
]

from django.urls import path

from .views import (
    FacultyCreationView,
    FacultyListView,
    FacultyDetailView,
    FacultyUpdateView,
    FacultyDeleteView,
)

app_name = 'Faculty'
urlpatterns = [
    path('add/', FacultyCreationView.as_view(), name='create'),
    path('list/', FacultyListView.as_view(), name='list'),
    path('detail/<slug:slug>/', FacultyDetailView.as_view(), name='detail'),
    path('edit/<slug:slug>/', FacultyUpdateView.as_view(), name='change'),
    path('delete/<slug:slug>/', FacultyDeleteView.as_view(), name='delete'),

]

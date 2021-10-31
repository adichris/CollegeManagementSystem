from django.urls import path

from .views import (
    ProgrammeListView,
    ProgrammeCreateView,
    ProgrammeDetailView,
    ProgrammeUpdateView,
    ProgrammeDeleteView
)

app_name = 'Programme'
urlpatterns = [
    path('list/', ProgrammeListView.as_view(), name='list'),
    path('add/', ProgrammeCreateView.as_view(), name='create'),
    path('<slug:slug>/', ProgrammeDetailView.as_view(), name='detail'),
    path('change/<slug:slug>/', ProgrammeUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', ProgrammeDeleteView.as_view(), name='delete'),

]

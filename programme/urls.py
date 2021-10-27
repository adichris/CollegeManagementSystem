from django.urls import path

from .views import ProgrammeListView

app_name = 'Programme'
urlpatterns = [
    path('list/', ProgrammeListView.as_view(), name='list'),
]

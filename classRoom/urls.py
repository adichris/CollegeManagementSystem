from django.urls import path
from .views import (
    ClassRoomTemplateView
)

app_name = 'classRoom'

urlpatterns = [
    path('', ClassRoomTemplateView.as_view(), name='templateview'),
]


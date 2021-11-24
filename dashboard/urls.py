from django.urls import path
from .views import (
    AdminDashboardTemplateView,
)


app_name = 'Dashboard'
urlpatterns = [
    path('admin/', AdminDashboardTemplateView.as_view(), name='admin'),
]

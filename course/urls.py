from django.urls import path
from .views import (
    CourseCreationView,
    CourseDetailView
)

app_name = 'Course'
urlpatterns = [
    path('addnew/', CourseCreationView.as_view(), name='create'),
    path('detail/<str:code>/<int:id>/', CourseDetailView.as_view(), name='detail'),

]

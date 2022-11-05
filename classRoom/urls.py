from django.urls import path, include
from .views import (
    ClassRoomTemplateView,
    CourseKlassTemplateView,
)

app_name = 'classRoom'

course_urlpatterns = [
    path("<str:course_code>/", CourseKlassTemplateView.as_view(), name="course_classroom"),
]
urlpatterns = [
    path('', ClassRoomTemplateView.as_view(), name='templateview'),
    path("lecturer/", include(course_urlpatterns)),
]


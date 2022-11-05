from django.urls import path, include
from .views import (
    CourseCreationView,
    CourseDetailView,
    StudentCourseListView,
    get_students_other_courses,
    StaffCourseListView,
    StudentCourseDetail,
    LecturerCoursesListView,
    CourseAssignmentCreateView,
    CourseAssigmentUpdateView,
    get_lecturer_short_infor,
    remove_lecturer_from_course_history,
    LecturerCourseDetailView,
    get_course_details,
)

app_name = 'Course'

staff_urlpatterns = [
    path('all/', StaffCourseListView.as_view(), name='staff_all'),
]

course_assignment_urlpatterns = [
    path('toanotherlecturer/<str:course_code>/', CourseAssignmentCreateView.as_view(), name='assign2another'),
    path('updateassigment/<int:courseassignmentpk>/', CourseAssigmentUpdateView.as_view(), name='assign_update'),
    path('getlecturershrtinfo/<slug:user_slug>/<int:assignment_id>/', get_lecturer_short_infor, name='rm_lec_short_info'),
    path('rmelecturer4rmcoursehist/<str:course_code>/<int:course_assignment_id>/', remove_lecturer_from_course_history, name='assignment_rm_lec4rmhist')

]

student_urlpatterns = [
    path('othersc/', get_students_other_courses, name='student_viewmore'),
    path('thissemester/', StudentCourseListView.as_view(), name='student_current'),
    path('details/<course_code>/', StudentCourseDetail.as_view(), name='stu_details'),
]

lecturer_urlpatterns = [
    path('list/', LecturerCoursesListView.as_view(), name='lec_list'),
    path('details/<course_code>/', LecturerCourseDetailView.as_view(), name='lec_detail'),
]
api_urlpatterns = [
    path('<str:course_code>/details/', get_course_details, name='lec_detail_ajax'),
]
urlpatterns = [
    path('staff/', include(api_urlpatterns)),
    path('api/', include(staff_urlpatterns)),
    path('lecturer/', include(lecturer_urlpatterns)),
    path('addnew/', CourseCreationView.as_view(), name='create'),
    path('detail/<str:code>/<int:id>/', CourseDetailView.as_view(), name='detail'),
    path('student/', include(student_urlpatterns)),
    path('courseassignment/', include(course_assignment_urlpatterns)),
]

from django.shortcuts import get_object_or_404, reverse
from django.http import Http404
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Course, Programme, models, CourseAssignment

from .forms import (
    CourseCreationForm,
    CourseFilter,
    CourseAssignmentForm,
)
from system.models import SemesterAcademicYearModel
from INSTITUTION.utils import get_back_url, get_next_url
from django.http.response import JsonResponse


class CourseCreationView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseCreationForm
    permission_required = 'course.add_course'
    template_name = 'course/staff/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(CourseCreationView, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Course'
        ctx['header'] = 'New Course'
        try:
            ctx['topheader'] = Programme.objects.get(id=self.request.GET.get('prg'))
        except Programme.DoesNotExist:
            pass
        ctx['back_url'] = self.request.GET.get('back')
        return ctx

    def get_initial(self):
        initial = super(CourseCreationView, self).get_initial()
        initial['programme'] = self.request.GET.get('prg')
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CourseCreationView, self).form_valid(form)


class CourseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'course.view_course'
    template_name = 'course/staff/detail.html'
    model = Course

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, code=self.kwargs['code'], id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        ctx = super(CourseDetailView, self).get_context_data(**kwargs)
        ctx['title'] = '%s' % self.object
        ctx['course_assignment'] = self.get_course_assigment()
        ctx['back_url'] = self.request.GET.get('back') or self.object.programme.get_absolute_url()
        return ctx

    def get_course_assigment(self):
        return self.object.courseassignment_set.all()

    def get_back_url(self):
        return self.request.GET.get('back') or self.object.programme.get_absolute_url()


class StudentCourseListView(LoginRequiredMixin, ListView):
    template_name = 'course/student/home.html'
    model = Course
    course_query_var = "qcourse"

    def get_context_data(self, **kwargs):
        ctx = super(StudentCourseListView, self).get_context_data(**kwargs)
        ctx['title'] = 'Student Courses'
        ctx['header'] = 'Your Courses'
        ctx['course_query_var'] = self.course_query_var
        ctx['course_query_data'] = self.request.GET.get(self.course_query_var)
        ctx['current_semester'] = self.current_semester
        ctx['back_url'] = get_back_url(self.request) or reverse("Student:home")
        return ctx

    @property
    def current_semester(self):
        return SemesterAcademicYearModel.objects.filter(is_current=True).first()

    def get_queryset(self):
        student = self.get_student()
        searched_query = self.request.GET.get(self.course_query_var)
        filter_kwargs = dict(
            programme=student.programme,
        )
        if searched_query:
            return self.model.objects.filter(
                models.Q(code__icontains=searched_query) | models.Q(name__icontains=searched_query),
                **filter_kwargs
            )

        return self.model.objects.filter(
            semester=self.current_semester,
            level=student.level,
            **filter_kwargs)

    def get_student(self):
        return self.request.user.student


@login_required
def get_students_other_courses(request):
    student = request.user.student
    courses = Course.objects.filter(programme__student=student)
    data = [{'name': course.name, 'semester': course.semester.name,
             'lecturer': course.lecturer.profile.get_full_name() if course.lecturer else None,
             'level': str(course.level), 'link': reverse('Course:stu_details', kwargs={'course_code': course.code}), }
            for course in courses]
    return JsonResponse(data={
        "courses": data
    })


class StaffCourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = 'course.view_courses_list'
    template_name = 'course/staff/list.html'
    filter_form_cls = CourseFilter
    paginate_by = 100

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(StaffCourseListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'All Course'
        ctx['header'] = 'courses'
        ctx['back_url'] = get_back_url(self.request) or reverse('Dashboard:admin')
        ctx['total_course'] = self.model.objects.count()
        ctx['filter_form'] = self.get_form
        return ctx

    @property
    def get_form(self):
        form = self.filter_form_cls(data=self.request.POST or None)
        form.is_valid()
        return form

    def get_paginate_by(self, queryset):
        try:
            paginate_by = self.request.POST.get('paginate_by') or self.get_form.cleaned_data['paginate_by']
            self.request.session["paginate_by"] = paginate_by
            return paginate_by
        except AttributeError:
            return self.request.session.get("paginate_by") or 100

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        form = self.get_form
        if form.is_valid():
            clean_data = form.cleaned_data
            return self.model.objects.search(
                name_start=clean_data.get('name_start_with'),
                name=clean_data.get('name'),
                code=clean_data.get('course_code'),
                programme_name=clean_data.get('programme_name'),
            )
        else:
            return super(StaffCourseListView, self).get_queryset()


class StudentCourseDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    permission_required = 'course.view_course'
    template_name = 'course/student/details.html'
    permission_denied_message = 'You need permission to view course details'

    def get_context_data(self, **kwargs):
        ctx = super(StudentCourseDetail, self).get_context_data(**kwargs)
        ctx['title'] = '%s Details' % self.object
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(code=self.kwargs['course_code'])
        except self.model.DoesNotExist:
            raise Http404('The Course is not present!')


class LecturerCoursesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = 'course.view_courses_list'
    template_name = 'course/lecturer/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LecturerCoursesListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['back_url'] = get_back_url(self.request)
        ctx['header'] = 'Your Current Courses'
        ctx['title'] = 'Your Courses'
        ctx['q'] = self.request.GET.get('q')
        ctx['info'] = f""" "{ctx['q']}" matches """ if ctx['q'] else 'Showing'
        return ctx

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.search_by_name_code(query=query,
                                                          courseassignment__lecturer__profile=self.request.user,
                                                          courseassignment__is_tutor=True)
        return self.model.objects.filter(courseassignment__lecturer__profile=self.request.user,
                                         courseassignment__is_tutor=True)


class CourseAssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CourseAssignment
    permission_required = 'course.add_courseassignment'
    form_class = CourseAssignmentForm
    template_name = 'course/courseassignment/create.html'
    permission_denied_message = 'You need permission to assign course to a lecturer'

    def get_success_url(self):
        return get_next_url(self.request) or get_back_url(self.request)

    def get_context_data(self, **kwargs):
        ctx = super(CourseAssignmentCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Assign Course to Lecturer'
        ctx['header'] = "Select the lecturer"
        ctx['back_url'] = get_back_url(self.request)
        ctx['course_name'] = self.get_course().name
        return ctx

    def get_course(self):
        return get_object_or_404(Course, code=self.kwargs.get('course_code'))

    def get_initial(self):
        initial = super(CourseAssignmentCreateView, self).get_initial()
        if not initial:
            initial = {}
        initial['course'] = self.get_course()
        return initial

    def form_valid(self, form):
        form.instance.course = self.get_course()
        form.instance.assigned_by = self.request.user
        return super(CourseAssignmentCreateView, self).form_valid(form)


class CourseAssigmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'course.change_courseassignment'
    permission_denied_message = 'You need permission to change course assignment'
    model = CourseAssignment
    form_class = CourseAssignmentForm
    pk_url_kwarg = 'courseassignmentpk'
    template_name = 'course/courseassignment/create.html'

    def get_success_url(self):
        return get_back_url(self.request) or reverse('Course:detail', kwargs={'code': self.object.course.code,
                                                                              'id': self.object.course.id})

    def get_context_data(self, **kwargs):
        ctx = super(CourseAssigmentUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Change  Course Lecturer'
        ctx['back_url'] = get_back_url(self.request)
        ctx['course_name'] = self.object.course.name
        lecturer = self.object.course.lecturer
        if lecturer:
            ctx['lecturer_profile'] = lecturer.profile
        ctx['toupdate'] = True
        return ctx


@permission_required('course.delete_courseassignment')
@login_required
def remove_lecturer_from_course_history(request, course_assignment_id, course_code):
    assignment = CourseAssignment.objects.filter(id=course_assignment_id, course__code=course_code).first()
    if assignment:
        assignment.delete()
    return JsonResponse({
        'isDeleted': True,
        'description': str(assignment.lecturer) + ' as been removed successfully'
    })


@permission_required('accounts.view_user')
@login_required
def get_lecturer_short_infor(request, user_slug, assignment_id):
    try:
        assignment = CourseAssignment.objects.get(lecturer__profile__slug=user_slug, id=assignment_id)
        user = assignment.lecturer.profile
    except CourseAssignment.DoesNotExist:
        data = {
            'description': 'Sorry, we can not fetch that information now'
        }
    else:
        data = {
            'full_name': user.get_full_name(),
            'department': user.get_department().name,
            'picture_src': user.picture.url,
            'email': user.email,
            'assignId': assignment.id,
            'removedUrl': reverse('Course:assignment_rm_lec4rmhist',
                                  kwargs={'course_code': assignment.course.code,
                                          'course_assignment_id': assignment.id})
        }
    return JsonResponse(data)


class LecturerCourseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    template_name = 'course/lecturer/detail.html'
    permission_required = 'course.view_lecturer_details'
    permission_denied_message = 'You need permission to view course details'

    def get_context_data(self, **kwargs):
        ctx = super(LecturerCourseDetailView, self).get_context_data(**kwargs)
        ctx['title'] = 'Course Details'
        ctx['back_url'] = get_back_url(self.request)
        ctx['recentActivity'] = None
        ctx['noRecentActivityMsg'] = 'After you\'ve start an activity, we\'ll show the most recent ones here.'
        return ctx

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(code=self.kwargs['course_code'])
        except self.model.DoesNotExist:
            return Http404('Course (%s) not found' % self.kwargs['course_code'])

    def get_lecturer(self):
        lecturer = self.request.user.lecturer
        if lecturer:
            return lecturer
        else:
            raise None


@login_required
def get_lecturer_course_details(request, course_code):
    try:
        course = Course.objects.get(
            code=course_code,
            courseassignment__lecturer__profile=request.user,
        )

        if course.lecturer == request.user.lecturer:
            return JsonResponse({
                'description': course.description,
                'creditHours': course.credit_hours,
                'programme': course.programme.name,
                'semester': course.semester.name,
                'academicYear': course.semester.academic_year,
                'level': str(course.level),
                'lecturer': course.lecturer.profile.get_full_name(),
                'Assessment':  3,
                'name': course.name,
                'code': course.code,
                'success': True,
            })
        else:
            return JsonResponse({
                'description': 'Sorry we can not show you details of this course\nBecause of your profile.'
            })
    except Course.DoesNotExist:
        return JsonResponse({
            'description': 'Sorry we can not show you details of this course\nBecause of your profile.'
        })


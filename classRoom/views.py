from django.db.models import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from INSTITUTION.utils import get_back_url
from course.models import CourseAssignment, Course
from django.http.response import Http404, HttpResponseForbidden


class ClassRoomTemplateView(LoginRequiredMixin, TemplateView):
    # template_name = 'classRoom/self/templateview.html'
    template_name = 'classRoom/self/templateview.html'

    def get_context_data(self, **kwargs):
        ctx = super(ClassRoomTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Class'
        ctx['back_url'] = get_back_url(self.request)
        ctx['user'] = self.request.user
        ctx['courses'] = self.get_courses()
        return ctx

    def get_courses(self):
        if self.request.user.is_teaching_staff:
            return [c.course for c in
                    CourseAssignment.lecturer_objects.get_lecturer_courses(self.request.user.identity)]
        elif self.request.user.is_student:
            return Course.objects.get_for_programme(self.request.user.student.programme.id)


class CourseKlassTemplateView(LoginRequiredMixin, TemplateView):
    # template_name = "classRoom/lecturer/template.html"
    template_name = "classRoom/lecturer/template.html"

    def get_context_data(self, **kwargs):
        ctx = super(CourseKlassTemplateView, self).get_context_data(**kwargs)
        ctx["title"] = '%s Classroom' % self.lecturer
        ctx["user"] = self.request.user
        ctx["course"] = self.course_instance
        return ctx

    @property
    def lecturer(self):
        try:
            return self.request.user.lecturer
        except ObjectDoesNotExist:
            return None

    @property
    def student(self):
        try:
            return self.request.user.student
        except ObjectDoesNotExist:
            return None

    @property
    def course_instance(self):
        try:
            if self.student:
                return Course.objects.get(
                    code=self.kwargs["course_code"],
                    programme__student=self.student
                )
            elif self.lecturer:
                return Course.objects.get(
                    code=self.kwargs["course_code"],
                    courseassignment__lecturer__identity=self.lecturer.identity,
                    courseassignment__is_tutor=True
                )
            else:
                raise Http404("")
        except Course.DoesNotExist as err:
            raise Http404(err)

    def get_page_header(self):
        return "%s Classroom" % self.course_instance

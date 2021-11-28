from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Course, Programme
from .forms import (
    CourseCreationForm
)
# Create your views here.


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
        ctx['back_url'] = self.request.GET.get('back') or self.object.programme.get_absolute_url()
        return ctx

    def get_back_url(self):
        return self.request.GET.get('back') or self.object.programme.get_absolute_url()

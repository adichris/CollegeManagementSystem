from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.models import Permission,  Group
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from INSTITUTION.views import JsonResponseMixin
from .models import SemesterModel
from .forms import (
    SemesterCreationForm,
    GroupCreationForm
)


class SemesterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SemesterModel
    form_class = SemesterCreationForm
    permission_required = 'system.add_semestermodel'
    template_name = 'system/semester/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(SemesterCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Add semester'
        ctx['header'] = 'New Semester'
        ctx['back_url'] = self.request.GET.get('back') or None
        return ctx

    def get_success_url(self):
        return reverse('System:semester_academic_year')


class SemesterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SemesterModel
    form_class = SemesterCreationForm
    permission_required = 'system.change_semestermodel'
    template_name = 'system/semester/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(SemesterUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Change semester'
        ctx['header'] = 'Change %s' % self.object
        ctx['back_url'] = self.request.GET.get('back') or None
        return ctx

    def get_success_url(self):
        return reverse('System:semester_academic_year')

    def get_object(self, *args):
        return get_object_or_404(
            self.model,
            name=self.kwargs.get('name'),
            id=self.kwargs.get('id'),
        )


class SemesterAcademicYearView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'system/semesteracademicyear.html'
    model = SemesterModel
    permission_required = 'system.view_semestermodel'

    def get_context_data(self, **kwargs):
        ctx = super(SemesterAcademicYearView, self).get_context_data(**kwargs)
        ctx['title'] = 'Semester and Academic Years'
        ctx['academic_year'] = self.get_academic_year()
        return ctx

    def get_academic_year(self):
        # return (CURRENT, NEXT) academic_semester
        return '2021 / 2022', '2022 / 2023'


class PermissionGroupListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Group
    template_name = 'system/permission/group/list.html'
    permission_required = 'contenttype.view_contenttype'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(PermissionGroupListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'Permission Groups'
        return ctx


class PermissionGroupCreate(PermissionRequiredMixin, LoginRequiredMixin, JsonResponseMixin, CreateView):
    permission_required = 'auth.add_group'
    model = Group
    form_class = GroupCreationForm
    template_name = 'system/'

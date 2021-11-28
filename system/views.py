from django.shortcuts import reverse, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.models import Permission,  Group

# Create your views here.
from INSTITUTION.views import JsonResponseMixin
from .models import SemesterModel, Level
from .forms import (
    SemesterCreationForm,
    GroupCreationForm,
    LevelCreationForm
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
    level_form = LevelCreationForm

    def get_context_data(self, **kwargs):
        ctx = super(SemesterAcademicYearView, self).get_context_data(**kwargs)
        ctx['title'] = 'Semester and Academic Years'
        ctx['academic_year'] = self.get_academic_year()
        ctx['levels'] = self.get_levels()
        ctx['level_Mtitel'] = self.get_course_modal_title()
        ctx['level_form'] = self.level_form(self.request.POST or None)

        return ctx

    def get_academic_year(self):
        # return (CURRENT, NEXT) academic_semester
        return '2021 / 2022', '2022 / 2023'

    def get_levels(self):
        return Level.objects.all()

    def get_course_modal_title(self):
        return 'Add Level'

    def post(self, request, *args, **kwargs):
        level_form = self.level_form(request.POST)
        self.object_list = self.model.objects.all()
        if level_form.is_valid():
            level_instance = level_form.save(True)
        ctx = self.get_context_data()
        ctx['level_form'] = level_form
        return render(request, self.template_name, ctx)


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


class LevelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'system.add_level'
    template_name = 'system/level/staff/add.html'
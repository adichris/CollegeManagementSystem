from django.shortcuts import reverse, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView
from django.contrib.auth.models import Permission,  Group
from django.http import Http404

# Create your views here.
from INSTITUTION.views import JsonResponseMixin
from INSTITUTION.utils import get_back_url
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
    template_name = 'system/staff/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(PermissionGroupCreate, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Permission Group'
        ctx['header'] = 'Group Details'
        ctx['back_url'] = get_back_url(self.request)

        return ctx

    def get_success_url(self):
        return reverse('System:permission_group_detail', kwargs={
            'pk': self.object.pk
        })


class PermissionGroupDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Group
    permission_required = 'auth.view_group'
    permission_denied_message = 'You need authentication permission to view this permission group'
    template_name = 'system/permission/group/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(PermissionGroupDetails, self).get_context_data(**kwargs)
        ctx['title'] = str(self.object) + ' Detail'
        ctx['permission_list'] = self.get_group_permissions()
        ctx['member_list'] = self.get_group_members()
        ctx['back_url'] = get_back_url(self.request) or reverse('System:permission_group')
        return ctx

    def get_group_permissions(self):
        return self.object.permissions.all()

    def get_group_members(self):
        return self.object.user_set.all()


class PermissionDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'auth.view_permission'
    model = Permission
    template_name = 'system/permission/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(PermissionDetail, self).get_context_data(**kwargs)
        ctx['title'] = '%s Permission Detail' % self.object
        ctx['groups'] = self.get_groups()
        return ctx

    def get_object(self, queryset=None):
        return self.model.objects.get(
                pk=self.kwargs['permission_pk']
        )

    def get_groups(self):
        return self.object.group_set.all()


class LevelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'system.add_level'
    template_name = 'system/level/staff/add.html'


class AddPermissionTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'system/permission/add.html'
    permission_model = Permission
    permission_required = 'auth.add_permission'
    permission_denied_message = 'You need permission to change permission-group permission'

    def get_permissions_group(self):
        try:
            return Group.objects.get(pk=self.kwargs['group_pk'], name=self.kwargs['group_name'])
        except Group.DoesNotExist:
            raise Http404('The Page your looking for does not exist')

    def get_context_data(self, **kwargs):
        group = self.get_permissions_group()
        ctx = super(AddPermissionTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Alter "%s" Permissions' % group
        ctx['groups'] = group
        ctx['current_permissions'] = group.permissions.all()

        return ctx

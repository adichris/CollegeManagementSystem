from django.shortcuts import reverse, get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView, View
from django.contrib.auth.models import Permission, Group
from django.http import Http404
from django.contrib.auth import get_user
from django.contrib.contenttypes.models import ContentType

from INSTITUTION.views import JsonResponseMixin, JsonResponse
from INSTITUTION.utils import get_back_url
from accounts.models import User
from .models import SemesterAcademicYearModel, Level
from .forms import (
    SemesterCreationForm,
    GroupCreationForm,
    LevelCreationForm,
    GroupPermissionAlterForm
)


class SemesterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SemesterAcademicYearModel
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
    model = SemesterAcademicYearModel
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
    model = SemesterAcademicYearModel
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
        # return (CURRENT, NEXT) academic_semester in tuple/list
        academic_year = self.model.objects.filter(is_current=True).first()
        nxt_academic_yr = int(academic_year.academic_year.split('/')[-1])
        return academic_year.get_academic_year_display(), (nxt_academic_yr, nxt_academic_yr + 1)

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
        ctx['member_count'] = self.get_group_members()
        ctx['back_url'] = get_back_url(self.request) or reverse('System:permission_group')
        return ctx

    def get_group_permissions(self):
        return self.object.permissions.all()

    def get_group_members(self):
        return self.object.user_set.count()

    def post(self, request, *args, **kwargs):
        response = self.get(request, *args, **kwargs)
        permission_name = request.POST.get('p_name')
        permission_pk = request.POST.get('p_pk')
        if permission_pk and permission_pk:
            try:
                permission_obj = Permission.objects.get(name=permission_name, pk=permission_pk)
                self.object.permissions.remove(permission_obj)
            except Permission.DoesNotExist:
                pass
        return response


class PermissionDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('auth.view_permission', 'auth.change_group')
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


class AddPermissionTemplateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'system/permission/add.html'
    permission_model = Permission
    permission_required = 'auth.add_permission'
    permission_denied_message = 'You need permission to change permission-group permission'
    model = Group
    form_class = GroupPermissionAlterForm

    def get_object(self, queryset=None):
        try:
            return Group.objects.get(pk=self.kwargs['group_pk'], name=self.kwargs['group_name'])
        except Group.DoesNotExist:
            raise Http404('The Page your looking for does not exist')

    def get_context_data(self, **kwargs):
        ctx = super(AddPermissionTemplateView, self).get_context_data(**kwargs)
        group = self.object
        ctx['title'] = 'Alter "%s" Permissions' % group
        ctx['group'] = group
        ctx['back_url'] = get_back_url(self.request)
        ctx['content_types'] = self.get_all_contenttypes()
        return ctx

    def get_permissions_set(self):
        return self.permission_model.objects.all()

    def get_all_contenttypes(self):
        return ContentType.objects.exclude(app_label__in=('admin', 'auth', 'contenttypes', 'sessions'))

    def get_success_url(self):
        return reverse('System:permission_group_detail', kwargs={
            'pk': self.object.pk
        })


def get_permission_ajax(request, permission_pk):
    try:
        perm = Permission.objects.get(pk=permission_pk)
        return JsonResponse({
            'p_name': perm.name,
            'p_pk': perm.pk,
            'p_cd': perm.codename,
            'p_ctt': str(perm.content_type),
        })
    except Permission.DoesNotExist as err:
        return JsonResponse({
            'error': err,
        })


def get_group_members_ajax(request, group_name):
    members = User.objects.filter(groups__name=group_name)
    data = [
        {
            'name': member.get_full_name(),
            'identity': member.identity,
            'type': member.get_category(),
            'url': reverse('System:get_user_shortInfo', kwargs={'identity': member.identity, 'group_name': group_name})
        }
        for member in members
    ]
    return JsonResponse({'data': data})


def remove_group_member(request, group_name, member_identity):
    if request.user.is_authenticated:
        user = get_user(request)
        try:
            group = Group.objects.get(name=group_name)
            member = User.objects.get(identity=member_identity)
        except Group.DoesNotExist or User.DoesNotExist:
            pass
        else:
            if user.has_perm('change_group', group):
                member.groups.remove(group)
                return JsonResponse({
                    'success': True,
                    'description': f'Successfully removed {member.get_full_name()} from {group.name}.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'description': f'Can not remove {member.get_full_name()} from {group.name}.<br> Permission denied'
                })
    return {
        'description': 'Not Found!'
    }


def get_group_member_information(request, identity, group_name):
    if not (request.user.is_authenticated and request.user.is_active):
        return
    try:
        user = User.objects.get(identity=identity, groups__name=group_name)
    except User.DoesNotExist:
        pass
    else:
        data = {
            'identity': user.identity,
            'name': user.get_full_name(),
            'shortName': user.get_short_name(),
            'department': user.get_department().name,
            'email': user.email,
            'removeMemberUrl': reverse('System:remove_group_member', kwargs={
                'group_name': group_name,
                'member_identity': user.identity
            })
        }
        return JsonResponse(data)


class AddMemberToPermissionGroup(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'auth.change_group'
    template_name = 'system/permission/group/addmember.html'
    model = Group

    def get_context_data(self, **kwargs):
        group_instance = self.get_object()
        ctx = super(AddMemberToPermissionGroup, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Group Member'
        ctx['back_url'] = get_back_url(self.request)
        ctx['group'] = group_instance
        ctx['is_student'] = 'student' in group_instance.name.lower()
        if self.request.POST:
            ctx['is_added'] = self.add_member()
        return ctx

    def get_object(self):
        try:
            return self.model.objects.get(name=self.kwargs['group_name'], pk=self.kwargs['group_pk'])
        except self.model.DoesNotExist:
            return Http404('Permission group does not exists')

    def add_student(self):
        students = User.objects.filter(student__is_active=True, is_active=True)
        self.get_object().user_set.add(*students)
        return students.count()

    def add_lecturers(self):
        lecturers = User.objects.filter(is_active=True, lecturer__is_active=True)
        self.get_object().user_set.add(*lecturers)
        return lecturers.count()

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def add_member(self):
        is_add_student = str(self.request.POST.get('addstudent')) == '1'
        is_add_lecturers = str(self.request.POST.get('addlecturers')) == '1'
        if is_add_student:
            returns = self.add_student()
            return returns
        elif is_add_lecturers:
            return self.add_lecturers()


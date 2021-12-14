from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, reverse

from .forms import DepartmentCreationForm, Department, DepartmentChangeForm
from programme.models import Programme
from .models import Faculty


def permission_denied_msg(perm='view'):
    return 'You need permission to %s department in the system'


class DepartmentsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Department
    permission_denied_message = permission_denied_msg('view')
    template_name = 'department/admin/list.html'
    permission_required = 'department.view_department'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentsListView, self).get_context_data(**kwargs)
        ctx['title'] = 'All Departments'
        ctx['header'] = 'All Departments'
        ctx["empty_text"] = self.get_empty_text()
        ctx['hasPerms'] = self.can_user_add_department()
        ctx['department_query'] = self.get_department_query()
        ctx['top_badge'] = self.get_top_badge()
        ctx['department_qry_cnt_msg'] = self.get_department_counts_msg()
        return ctx

    def get_top_badge(self):
        return ' %s' % self.model.objects.count()

    def get_department_counts_msg(self):
        counts = self.object_list.count()
        query = self.get_department_query()
        if query:
            if counts > 1:
                return f'"<b>{query}</b>" matches {counts} departments'
            return f'"<b>{query}</b>" match {counts} department'

    def get_department_query(self):
        return self.request.GET.get('department_query')

    def can_user_add_department(self):
        user = self.request.user
        return user.has_perm('department.add_department')

    def get_empty_text(self):
        query = self.get_department_query()
        if query:
            return f'"<b>{query}</b>" matches no department in the system'
        return 'There is no department in the system yet'

    def get_queryset(self):
        return self.model.objects.search(self.get_department_query())


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'department/admin/create.html'
    model = Department
    permission_required = 'department.add_department'
    permission_denied_message = permission_denied_msg('add')
    form_class = DepartmentCreationForm

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'New Department'
        ctx['header'] = 'Add Department'
        return ctx

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(DepartmentCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DepartmentCreateView, self).get_form_kwargs()
        faculty_slug = self.request.GET.get('facultyslug')
        if faculty_slug:
            kwargs['faculty_queryset'] = Faculty.objects.filter(slug=faculty_slug)
        return kwargs


class DepartmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_denied_message = permission_denied_msg('view')
    permission_required = 'department.view_department'
    model = Department
    template_name = 'department/admin/detail.html'
    page_by = 10

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentDetailView, self).get_context_data(**kwargs)
        ctx['title'] = '%s - detail' % self.object
        ctx['back_url'] = self.get_back_url()
        ctx['back_name'] = self.get_back_name()
        ctx['programmes_page'] = self.programmes_paginator()
        ctx['lecturers'] = self.get_lecturers()
        ctx['can_add_lecturer'] = self.can_add_lecturer()
        return ctx

    def get_department_programmes(self):
        return Programme.objects.filter(department=self.object)

    def programmes_paginator(self):
        page_number = self.request.GET.get('page')
        paginator = Paginator(self.get_department_programmes(), per_page=self.page_by)
        page_object = paginator.get_page(page_number)
        return page_object

    def get_back_url(self):
        return self.request.GET.get('back')

    def get_back_name(self):
        return self.request.GET.get('backname') or 'back'

    def get_lecturers(self):
        return self.object.best_lecturers

    def can_add_lecturer(self):
        return self.request.user.has_perm('add_lecturer')


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    template_name = 'department/admin/create.html'
    form_class = DepartmentChangeForm
    permission_required = 'department.change_department'
    permission_denied_message = permission_denied_msg('change')

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Change %s' % self.object.name
        ctx['header'] = ctx['title']
        return ctx

    def get_success_url(self):
        return self.object.get_absolute_url()


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    permission_required = 'department.delete_department'
    permission_denied_message = permission_denied_msg('delete')
    template_name = 'department/admin/delete.html'

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = 'Delete %s ' % self.object.name
        return ctx

    def get_success_url(self):
        return reverse('Faculty:list')


class FacultyDepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'department.view_department'
    permission_denied_message = permission_denied_msg('view')
    model = Department
    template_name = "department/admin/list.html"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(FacultyDepartmentListView, self).get_context_data(object_list=object_list, **kwargs)
        self.faculty = self.get_faculty()
        ctx['title'] = '%s: Departments' % self.faculty
        ctx['header'] = '%s' % self.faculty
        ctx['subheader'] = 'Departments'
        ctx['faculty_sug'] = self.faculty.slug
        ctx["empty_text"] = self.get_empty_text()
        ctx['hasPerms'] = self.can_user_add_department()
        ctx['department_query'] = self.get_department_query()
        ctx['back_url'] = self.faculty.get_absolute_url()
        ctx['back_name'] = self.faculty.name
        ctx['top_badge'] = self.get_top_badge()
        ctx['department_qry_cnt_msg'] = self.get_department_counts_msg()
        return ctx

    def get_department_query(self):
        return self.request.GET.get('department_query')

    def can_user_add_department(self):
        user = self.request.user
        return user.has_perm('department.add_department')

    def get_empty_text(self):
        query = self.get_department_query()
        if query:
            return f'"<b>{query}</b>" matches no department in {self.faculty}'
        return 'There is no department in the system yet'

    def get_faculty(self):
        return get_object_or_404(
            Faculty,
            slug=self.kwargs['faculty_slug'],
        )

    def get_queryset(self):
        return self.model.objects.get_for_faculty(
            faculty_slug=self.kwargs['faculty_slug'],
            query=self.get_department_query()
        )

    def get_top_badge(self):
        return '%s' % self.model.objects.get_for_faculty(faculty_slug=self.kwargs['faculty_slug']).count()

    def get_department_counts_msg(self):
        counts = self.object_list.count()
        query = self.get_department_query()
        if query:
            if counts > 1:
                return f'"<b>{query}</b>" matches {counts} departments'
            return f'"<b>{query}</b>" match {counts} department'

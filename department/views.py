from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .forms import DepartmentCreationForm, Department


def permission_denied_msg(perm='view'):
    return 'You need permission to %s department in the system'


class DepartmentsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Department
    permission_denied_message = permission_denied_msg('view')
    template_name = 'department/admin/list.html'
    permission_required = 'department.view_department'

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentsListView, self).get_context_data(**kwargs)
        ctx['title'] = 'All Departments'
        ctx['header'] = 'All Departments'
        ctx["empty_text"] = self.get_empty_text()
        ctx['hasPerms'] = self.can_user_add_department()
        ctx['department_query'] = self.get_department_query()
        return ctx

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


class DepartmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_denied_message = permission_denied_msg('view')
    permission_required = 'department.view_department'
    model = Department
    template_name = 'department/admin/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(DepartmentDetailView, self).get_context_data(**kwargs)
        ctx['title'] = '%s - detail' % self.object

        return ctx


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    template_name = 'department/admin/create.html'
    form_class = DepartmentCreationForm
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



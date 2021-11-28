from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import reverse
from django.core.exceptions import FieldDoesNotExist

from .forms import Programme, ProgrammeCreationForm
from course.models import Course
from .models import Department


def permission_denied_msg(perm='view'):
    return 'You need permission to %s programme in the system'


class ProgrammeListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Programme
    template_name = 'programme/admin/list.html'
    permission_required = 'programme.add_programme'
    permission_denied_message = permission_denied_msg('add')
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(ProgrammeListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'All Programmes'
        ctx['has_perm'] = self.can_user_add_programme()
        ctx['programme_query'] = self.get_programme_query()
        ctx['p_counts_msg'] = self.get_programme_counts_msg()
        ctx['empty_text'] = self.get_empty_text()
        ctx['total_programmes'] = self.get_total_programmes()
        return ctx

    def get_total_programmes(self):
        return self.model.objects.count()

    def get_empty_text(self):
        query = self.get_programme_query()
        if query:
            return f'"<b>{query}</b>" matches nothing.<p>search programmes by their name </p>'
        return 'There is no programme in the system yet.'

    def get_programme_counts_msg(self):
        counts = self.object_list.count()
        msg = f'{counts} Programme'
        query = self.get_programme_query()
        if counts > 1 and query:
            msg = f'"<b>{query}</b>" matches {counts} programme'
        if counts > 1:
            msg += 's'
        elif counts == 0:
            return
        return msg

    def can_user_add_programme(self):
        return self.request.user.has_perm('programme.add_programme')

    def get_programme_query(self):
        return self.request.GET.get('programmeQuery')

    def get_queryset(self):
        return self.model.objects.search(self.get_programme_query())


class ProgrammeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Programme
    form_class = ProgrammeCreationForm
    template_name = 'programme/admin/create.html'
    permission_required = 'programme.add_programme'
    permission_denied_message = permission_denied_msg('add')

    def get_context_data(self, **kwargs):
        ctx = super(ProgrammeCreateView, self).get_context_data(**kwargs)
        ctx['header'] = 'Add Programme'
        ctx['title'] = 'New Programme'
        return ctx

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        department_slug = self.request.GET.get('departmentslug')
        kwargs = super(ProgrammeCreateView, self).get_form_kwargs()
        if department_slug:
            department_queryset = Department.objects.filter(slug=department_slug)
            self.department = department_queryset.first()
            if department_queryset.exists:
                kwargs['department_queryset'] = department_queryset
        return kwargs


class ProgrammeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Programme
    template_name = 'programme/admin/view.html'
    permission_required = 'programme.add_programme'
    permission_denied_message = permission_denied_msg('add')

    def get_context_data(self, **kwargs):
        ctx = super(ProgrammeDetailView, self).get_context_data(**kwargs)
        ctx['header'] = 'Add Programme'
        ctx['title'] = '%s Programme' % self.object.name
        ctx['backname'] = self.get_back_name()
        ctx['backurl'] = self.get_back_url()
        ctx['programme_courses'] = self.get_programme_courses()
        ctx['students'] = self.get_students()
        return ctx

    def get_back_url(self):
        try:
            return self.request.GET.get('back') or self.object.department.get_absolute_url()
        except FieldDoesNotExist:
            return reverse('Department:Programme:list')

    def get_back_name(self):
        try:
            return self.request.GET.get('backname') or self.object.department.name
        except FieldDoesNotExist:
            return 'Programmes'

    def get_programme_courses(self):
        return Course.objects.get_for_programme(self.object.id)

    def get_students(self):
        return


class ProgrammeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Programme
    template_name = 'programme/admin/create.html'
    permission_required = 'programme.change_programme'
    permission_denied_message = permission_denied_msg('change')
    form_class = ProgrammeCreationForm

    def get_context_data(self, **kwargs):
        ctx = super(ProgrammeUpdateView, self).get_context_data(**kwargs)
        ctx['header'] = 'Change %s' % self.object.name
        ctx['title'] = 'Change %s' % self.object.name
        return ctx


class ProgrammeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programme/admin/delete.html'
    permission_required = 'programme.delete_programme'
    permission_denied_message = permission_denied_msg('delete')

    def get_context_data(self, **kwargs):
        ctx = super(ProgrammeDeleteView, self).get_context_data(**kwargs)
        ctx['header'] = 'Delete %s' % self.object.name
        ctx['title'] = 'Delete %s' % self.object.name
        return ctx


# TODO DepartmentProgrammesListView

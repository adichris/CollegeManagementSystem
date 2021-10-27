from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import Faculty, FacultyCreationForm, FacultyChangeForm


class FacultyCreationView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Faculty
    form_class = FacultyCreationForm
    template_name = 'faculty/admin/create.html'
    permission_required = 'faculty.add_faculty'
    permission_denied_message = 'You need permission to add faulty'

    def get_context_data(self, **kwargs):
        ctx = super(FacultyCreationView, self).get_context_data(**kwargs)
        ctx['title'] = 'Add Faculty'
        ctx['header'] = 'Add New Faculty'
        return ctx

    def get_success_url(self):
        return self.object.get_absolute_url()


class FacultyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Faculty
    permission_required = 'faculty.view_faculty'
    template_name = 'faculty/admin/listview.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(FacultyListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'Faculties'
        ctx['header'] = 'All Faculties in this Institution'
        ctx['empty_text'] = 'There are no faculties in the system'
        ctx['facultyQry'] = self.searched_query
        ctx['hadPerms'] = self.request.user.has_perms(*('faculty.change_faculty',  'faculty.add_faculty'))
        return ctx

    @property
    def searched_query(self):
        return self.request.GET.get('facultyQry')

    def get_login_url(self):
        return reverse('Home:login')

    def get_queryset(self):
        return self.model.objects.search(self.searched_query)


class FacultyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'faculty/admin/view.html'
    model = Faculty
    permission_required = 'faculty.view_faculty'

    def get_context_data(self, **kwargs):
        ctx = super(FacultyDetailView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name + ' - details'
        return ctx


class FacultyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Faculty
    template_name = 'faculty/admin/edit.html'
    permission_required = 'faculty.change_faculty'
    form_class = FacultyChangeForm

    def get_context_data(self, **kwargs):
        ctx = super(FacultyUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Edit %s' % self.object.name
        ctx['header'] = 'Edit %s Faculty' % self.object.name
        return ctx


class FacultyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Faculty
    template_name = 'faculty/admin/delete.html'
    permission_required = 'delete_faculty'
    permission_denied_message = 'You need permission to delete this faculty from the system'

    def get_context_data(self, **kwargs):
        ctx = super(FacultyDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = 'Delete %s' % self.object.name
        ctx['header'] = 'Delete %s' % self.object.name
        return ctx

    def get_success_url(self):
        return reverse('Faculty:list')

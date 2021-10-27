from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .forms import Programme, ProgrammeCreationForm


class ProgrammeListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Programme

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(ProgrammeListView, self).get_context_data(object_list=object_list, **kwargs)
        ctx['title'] = 'All Programmes'
        return ctx


class ProgrammeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Programme
    form_class = ProgrammeCreationForm
    template_name = 'programme/admin/list.html'
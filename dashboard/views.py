from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.response import HttpResponseForbidden


class AdminDashboardTemplateView(TemplateView, LoginRequiredMixin):
    template_name = 'dashboard/admin/main.html'

    def get_context_data(self, **kwargs):
        ctx = super(AdminDashboardTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Dashboard'
        return ctx

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(AdminDashboardTemplateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from INSTITUTION.utils import get_back_url
# Create your views here.


class ClassRoomTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'classRoom/self/templateview.html'

    def get_context_data(self, **kwargs):
        ctx = super(ClassRoomTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Class'
        ctx['back_url'] = get_back_url(self.request)
        ctx['user'] = self.request.user
        return ctx

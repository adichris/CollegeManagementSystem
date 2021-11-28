from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class StaffLecturerTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'lecturer/staff/template.html'

    def get_context_data(self, **kwargs):
        ctx = super(StaffLecturerTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Lecturers'
        return ctx

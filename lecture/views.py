from typing import Any, Dict
from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView, ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.response import Http404, JsonResponse
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from INSTITUTION.utils import get_back_url, get_next_url
from CollegeManagementSystem.validation import is_safe_query
from .models import Lecturer

from .forms import (
    LecturerApplicationChangeForm,
    DepartmentAssigmentForm,
    # InitialCreationForm
)


class StaffLecturerTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'lecturer/staff/template.html'

    def get_context_data(self, **kwargs):
        ctx = super(StaffLecturerTemplateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Lecturers'
        return ctx


class AddLecturerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "lecturer/staff/add.html"
    permission_required = 'lecture.add_lecturer'
    permission_denied_message = 'You need permission to add a lecturer'

    # form_class = InitialCreationForm
    # model = Lecturer

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Add Lecturer'
        }
        return context

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        err_msg = None
        try:
            identity_data = request.POST['identity']
            is_active_data = request.POST['is_active'] == 'on'
            lecturer, created = Lecturer.objects.get_or_create(
                identity=identity_data,
                is_active=is_active_data
            )
            uncompleted = not (lecturer.profile and lecturer.application_letter and lecturer.cv and lecturer.department)
            if created or uncompleted:
                return redirect('Accounts:create_lecturer', identity=identity_data)
            else:
                err_msg = "Lecturer with that identity already exist"
        except KeyError:
            err_msg = 'Lecturer Identity is required'
        else:
            ctx['identity'] = identity_data
        ctx['err_msg'] = err_msg
        return render(request, self.template_name, ctx)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class AddLecturerTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = Lecturer
    template_name = 'lecturer/staff/add_template.html'
    permission_required = ('lecture.add_lecturer', 'lecture.change_lecturer')
    completed_var = 'completed'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        lecturer = self.get_lecturer()
        ctx['title'] = 'Add Lecture Details'
        ctx['has_employment_history'] = self.has_employment_history()
        ctx['has_app'] = self.has_application()
        ctx['has_department'] = self.has_department()
        ctx['has_course'] = self.has_courses()
        ctx['profile_slug'] = self.profile.slug
        ctx['identity'] = lecturer.identity
        ctx['completed_var'] = self.completed_var
        ctx['is_allowed2complete'] = ctx['has_app'] and ctx['has_employment_history']
        if ctx['is_allowed2complete'] and not lecturer.is_active:
            lecturer.is_active = True
            lecturer.save()
        return ctx

    def get_lecturer(self):
        self.lecturer = Lecturer.objects.get(identity=self.kwargs['identity'])
        self.profile = self.lecturer.profile

        return self.lecturer

    def has_employment_history(self):
        try:
            return self.lecturer.profile.employment_history
        except ObjectDoesNotExist:
            return

    def has_application(self):
        return bool(self.lecturer.application_letter or self.lecturer.cv)

    def has_department(self):
        return bool(self.lecturer.department)

    def has_courses(self):
        return

    def get(self, request, *args, **kwargs):
        if request.GET.get(self.completed_var) == '1':
            return redirect('Lecturer:staff_template')
        else:
            return super(AddLecturerTemplateView, self).get(request, *args, **kwargs)


class LecturerApplicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('lecture.add_lecturer', 'lecture.change_lecturer')
    permission_denied_message = 'You need permission change lecturer application information'
    model = Lecturer
    template_name = 'lecturer/staff/application_change.html'
    form_class = LecturerApplicationChangeForm

    def get_context_data(self, **kwargs):
        ctx = super(LecturerApplicationCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Change Lecturer Application'
        ctx['header'] = 'Lecturer Application'
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def get_success_url(self):
        redirect_to = get_next_url(self.request) or get_back_url(self.request)
        if redirect_to:
            return redirect_to
        return super(LecturerApplicationCreateView, self).get_success_url()

    def get_object(self, queryset=None):
        return Lecturer.objects.get(
            identity=self.kwargs['identity']
        )


class LecturerDepartmentAssignment(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lecturer
    permission_required = 'lecture.assign_department'
    template_name = 'lecturer/staff/application_change.html'
    form_class = DepartmentAssigmentForm

    def get_context_data(self, **kwargs):
        ctx = super(LecturerDepartmentAssignment, self).get_context_data(**kwargs)
        ctx['title'] = 'Department Assignment'
        ctx['header'] = ctx['title']
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def get_success_url(self):
        redirect_to = get_next_url(self.request) or get_next_url(self.request)
        if redirect_to:
            return redirect_to
        else:
            return reverse('Lecturer:staff_add_template', kwargs={'identity': self.kwargs['identity']})

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(identity=self.kwargs['identity'])
        except self.model.DoesNotExist:
            raise Http404('The lecturer5 with that IDENTITY does not exist')


class LecturerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'lecture.list_lecturer'
    permission_denied_message = 'You need permission to view lecturer list'
    model = Lecturer
    template_name = 'lecturer/staff/listview.html'

    def get_query(self):
        query = self.request.GET.get('qlecturer')
        if is_safe_query(query):
            return query

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LecturerListView, self).get_context_data(object_list=object_list, **kwargs)
        department = self.get_department()
        if department:
            ctx['title'] = department.replace('-', ' ') + ' lecturers'
        else:
            ctx['title'] = 'All Lecturers'
        ctx['query'] = self.get_query()
        ctx['can_edit'] = self.can_edit()
        ctx['can_view'] = self.can_edit()
        ctx['back_url'] = get_back_url(self.request)
        return ctx

    def can_edit(self):
        return self.request.user.has_perm('lecture.add_lecturer')

    def can_view(self):
        return self.request.user.has_perm('lecture.view_lecturer')

    def get_queryset(self):
        department = self.get_department()
        if department:
            return self.model.objects.search(query=self.get_query(), department__slug=department)
        return self.model.objects.search(query=self.get_query())

    def get_department(self):
        return self.kwargs.get('department_slug')


class LecturerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'lecturer/self/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(LecturerDashboardView, self).get_context_data(**kwargs)
        # lecturer_instance = self.get_lecturer()
        ctx['title'] = 'Your Dashboard'
        return ctx

    def get_lecturer(self):
        return Lecturer.objects.get(profile_id=self.request.user.id)


@login_required
def get_my_information_ajax(request):
    data = {
        'description': 'Please try again.'
    }
    try:
        lecturer = Lecturer.objects.get(profile=get_user(request))
    except Lecturer.DoesNotExist:
        data = {
            'description': 'Your profile does not match any lecturer object.'
        }
    else:
        data = {
            'identity': lecturer.identity,
            'department': lecturer.department.name,
            'isActive': lecturer.is_active,
            'applicationLetter': lecturer.application_letter.url,
            'cv': lecturer.cv.url,
        }

    return JsonResponse(data)

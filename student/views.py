from django.shortcuts import resolve_url, get_object_or_404, reverse
from django.views.generic import RedirectView
from django.contrib.auth import login, logout
from accounts.models import User
from django.contrib.auth.models import Permission, Group
from .models import Student
from admission.models import StudentForms, FormStatusChoice


class StudentAdmissionRedirectView(RedirectView):
    #  check the admission status and redirect the student to the require path

    def get_redirect_url(self, *args, **kwargs):
        admission_form = get_object_or_404(StudentForms, serial_number=self.kwargs['serial_number'])
        if admission_form.status == FormStatusChoice.NEW:
            return reverse('Accounts:admission_student_profile', kwargs={
                "serial_number": admission_form.serial_number
            })

        if admission_form.status != FormStatusChoice.Expired:
            user = User.objects.get(identity=admission_form.serial_number)
            if self.request.user != user:
                if self.request.user.is_authenticated:
                    logout(request=self.request)
                login(user=user, request=self.request)

            student, created_student = Student.objects.get_or_create(
                admission_form_id=admission_form.id,
                profile_id=user.id
            )
            self.set_permissions_required()

            if admission_form.status == FormStatusChoice.AT_ADDRESS:
                return reverse('Address:admission_student_create')

            elif admission_form.status == FormStatusChoice.AT_EMPLOYMENT:
                return reverse('EmploymentHistory:student_admission_create_history')

            elif admission_form.status == FormStatusChoice.AT_SPONSOR:
                return reverse('Sponsor:student_admission')

        elif admission_form.status == FormStatusChoice.COMPLETED:
            pass

        else:
            pass

    def set_permissions_required(self):
        student_admission_grp, created = Group.objects.get_or_create(name='student admission')
        student_admission_grp.permissions.add(*Permission.objects.filter(
            codename__in=('add_employmenthistorymodel',
                          'change_employmenthistorymodel',
                          'add_studentsponsor',
                          'change_studentsponsor',
                          'add_address',
                          'change_address',
                          )
            ),
                                              )
        self.request.user.groups.add(student_admission_grp)

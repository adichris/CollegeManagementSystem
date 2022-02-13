import datetime
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as today_time
from django.shortcuts import reverse

from accounts.models import User
from admission.models import StudentForms
from programme.models import Programme
from system.models import Level


class StudentManager(models.Manager):
    def get_newly_admitted(self, query=None, **kwargs):
        if query:
            q_query = models.Q(profile__email__icontains=query) | \
                      models.Q(profile__first_name__icontains=query) | \
                      models.Q(profile__last_name__icontains=query) | \
                      models.Q(admission_form__serial_number__startswith=query) | \
                      models.Q(index_number__startswith=query)
            return self.filter(
                q_query,
                date_admitted__year=today_time().year,
                **kwargs
            )
        return self.filter(**kwargs)

    def get_all_sort(self, by, query=None):
        return self.all(query=query).order_by(by)

    def all(self, query=None, programme_slug=None, department_slug=None):
        return self.get_only_active(query=query, programme_slug=programme_slug, department_slug=department_slug)

    def get_programme_department_slugs_kwargs(self, programme_slug=None, department_slug=None):
        kwargs = {}
        if department_slug:
            kwargs['programme__department__slug'] = department_slug
        if programme_slug:
            kwargs['programme__slug'] = programme_slug
        return kwargs

    def get_only_active(self, query=None, programme_slug=None, department_slug=None):
        kwargs = self.get_programme_department_slugs_kwargs(
            programme_slug=programme_slug,
            department_slug=department_slug
        )
        if query:
            query_objs = models.Q(index_number__icontains=query) | \
                         models.Q(profile__email__icontains=query) | \
                         models.Q(profile__first_name__icontains=query) | \
                         models.Q(profile__last_name__icontains=query) | \
                         models.Q(profile__identity__icontains=query)
            return self.filter(
                query_objs,
                is_active=True,
                **kwargs
            )
        return self.filter(
            is_active=True,
            **kwargs
        )

    def get_active_and_old(self, programme_slug=None, department_slug=None):
        kwargs = self.get_programme_department_slugs_kwargs(programme_slug=programme_slug,
                                                            department_slug=department_slug)
        return self.filter(
            profile__is_active=True,
            date_completed__lt=today_time().date(),
            **kwargs
        )


class Student(models.Model):
    # add choice give field / programme
    profile = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   unique=True, related_name='student_profile',
                                   related_query_name='student', null=True
                                   )
    admission_form = models.OneToOneField(StudentForms, related_name='student_admission_form',
                                          on_delete=models.CASCADE, unique=True, null=True)
    index_number = models.CharField(null=True, max_length=60, unique=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    date_admitted = models.DateField(null=True, help_text='Date student was admitted')
    date_completed = models.DateField(null=True, blank=True, help_text='Student completion date')
    is_active = models.BooleanField(default=False, help_text='Is this student current or active')
    objects = StudentManager()

    @property
    def is_old(self):
        return self.date_completed < today_time().date()

    @property
    def full_name(self):
        return self.profile.get_full_name()

    def __str__(self):
        return str(self.profile)

    def get_previous_school(self):
        return self.previous_education.first() or '---'

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ('id', 'profile')
        permissions = [
            ('list_student', _('can view student list')),
            ('staff_view_student', _('can view student detail as staff')),
        ]

    def get_absolute_detailview4staff(self):
        return reverse('Student:staff_student_detail', kwargs={
            'profile__identity': self.profile.identity,
            'pk': self.pk,
        })

    @property
    def position_title(self):
        return 'Student'


class StudentProgrammeChoice(models.Model):
    first_choice = models.ForeignKey(Programme, related_name='first_choice', on_delete=models.CASCADE)
    second_choice = models.ForeignKey(Programme, related_name='second_choice', on_delete=models.CASCADE)
    third_choice = models.ForeignKey(Programme, related_name='third_choice', on_delete=models.CASCADE)
    student = models.OneToOneField(unique=True, to=Student, on_delete=models.CASCADE, related_name='programme_choices')

    class Meta:
        db_table = 'studentprogrammechoice'
        unique_together = ('first_choice', 'second_choice', 'student')

    def __str__(self):
        return str(self.first_choice)


def upload_certificate_copy_to(instance, filename):
    return os.path.join('student', instance.name, instance.slug, 'certificate_copy', filename)


class AdmissionCertificate(models.Model):
    student = models.OneToOneField(Student, related_name='cert_student',
                                   on_delete=models.CASCADE, unique=True)
    certificate_picture = models.FileField(
        null=True,
        upload_to=upload_certificate_copy_to,
        help_text=_(
            'Include all the necessary(WASSCE, NOV/DEC, HND, SRN, Diploma Cert, etc) certificate in one pdf file')
    )

    class Meta:
        db_table = 'student_admission_exam_certificate'

    def __str__(self):
        return str(self.student) + ' exam certificate'


class AdmissionExaminationTextChoice(models.TextChoices):
    PRIVATE_CANDIDATE = ('private candidate', 'Private Candidate')
    SCHOOL_CANDIDATE = ('school candidate', 'School Candidate')


EXAMINATION_YEAR_START = 1980
EXAMINATION_YEAR_END = datetime.date.today().year


class WaecGradeChoices(models.TextChoices):
    A1 = 'A1', 'A1'
    B2 = 'B2', 'B2'
    C3 = 'B3', 'B3'
    C4 = 'C4', 'C4'
    C5 = 'C5', 'C5'
    C6 = 'C6', 'C6'
    D7 = 'D7', 'D7'
    E8 = 'E8', 'E8'
    F9 = 'F9', 'F9'


def shs_subject_choices():
    from pathlib import Path
    subjects = None
    filepath = Path(__file__).parent / 'shs_subjects.csv'
    if filepath.is_file():
        with filepath.open('r') as file:
            subjects = tuple((subject.replace('\n', ''), subject.replace('\n', '')) for subject in set(file.readlines()))
    return subjects


def examination_year_tuple():
    """ :return  iterable containing (actual value, human readable name) tuples. """

    return tuple((yr, yr) for yr in range(EXAMINATION_YEAR_END, EXAMINATION_YEAR_START, -1))


class CertExamRecordManager(models.Manager):
    def get_for_certificate(self, certificate_id):
        return self.filter(certificate_id=certificate_id)


class CertExamRecord(models.Model):
    certificate = models.ForeignKey(AdmissionCertificate,
                                    on_delete=models.CASCADE,
                                    related_name='certificate_records',
                                    )
    subject = models.CharField(max_length=120, choices=shs_subject_choices())
    index_number = models.CharField(max_length=20, help_text=_('Examination number'))
    examination_year = models.IntegerField(choices=examination_year_tuple())
    school = models.CharField(max_length=200, help_text=_('School Name'), null=True, blank=True)
    grade = models.CharField(max_length=3, choices=WaecGradeChoices.choices)
    # TODO change grade to select field
    examination_type = models.CharField(max_length=120,
                                        choices=AdmissionExaminationTextChoice.choices,
                                        default=AdmissionExaminationTextChoice.SCHOOL_CANDIDATE
                                        )
    objects = CertExamRecordManager()

    class Meta:
        db_table = 'student_admission_exam_result'
        unique_together = ('certificate', 'examination_type', 'examination_year', 'subject')

    def __str__(self):
        return self.subject


class StudentPreviousEducation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='previous_education',
                                related_query_name='previous_education')
    school = models.CharField(max_length=200, help_text=_('Previous school name'))
    region = models.CharField(max_length=200, help_text=_('Region the school is located'))
    from_year = models.IntegerField(choices=examination_year_tuple())
    to_year = models.IntegerField(choices=examination_year_tuple())

    class Meta:
        db_table = 'studentpreviouseducation'
        verbose_name_plural = _('Student Previous Education')
        unique_together = (
            'student', 'school', 'to_year'
        )

    def __str__(self):
        return self.school


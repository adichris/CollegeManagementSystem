from django.db import models
from django.db.models import UniqueConstraint
from phonenumber_field.modelfields import PhoneNumberField
from CollegeManagementSystem.validation import validate_alphanumberic_space
from django.shortcuts import reverse


from INSTITUTION.utils import AcademicYear


class FormTypeManager(models.Manager):
    def get_for_form_batch_creation(self):
        return self.all()

    def search(self, value):
        if value:
            return self.filter(
                models.Q(title__icontains=value) | models.Q(subtitle__icontains=value)
            )
        return self.all()


class FormTypeChoicesModel(models.Model):
    title = models.CharField(max_length=120, validators=[validate_alphanumberic_space])
    subtitle = models.CharField(max_length=120, validators=[validate_alphanumberic_space])
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = FormTypeManager()

    class Meta:
        ordering = ('title', 'id')
        constraints = [
            UniqueConstraint(fields=['title', 'subtitle'], name='unique_formtype')
                       ]

    def get_absolute_url(self):
        return reverse('Admission:form_type_detail',
                       kwargs={
                           'title': self.title,
                           'id': self.id
                       })

    def get_absolute_update_url(self):
        return reverse('Admission:form_type_update',
                       kwargs={
                           'title': self.title,
                           'id': self.id
                       })

    def forms_referenced(self):
        return self.forms

    def __str__(self):
        return self.title + ' (%s)' % self.subtitle


class FormStatusChoice(models.TextChoices):
    COMPLETED = 'completed', 'Completed'
    SUBMITTED = 'submitted', 'Submitted'
    AT_PROFILE = 'at profile', 'At Profile'
    AT_ADDRESS = 'at address', 'At Address'
    AT_CERTIFICATION = 'at certification', 'At Certification'
    AT_EMPLOYMENT = 'at employment', 'At Employment History',
    AT_SPONSOR = 'at sponsor', 'AT SPONSORSHIP'
    AT_PROGRAMME = 'at programme', 'AT PROGRAMME'
    AT_EDUCATION = 'at education', 'AT EDUCATION'
    EXPIRED = 'expired', 'Expired'
    NEW = 'new', 'New'
    PROCESSING = 'processing', 'Processing'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'


class StudentFormsManager(models.Manager):
    def search(self, query, status=None):
        return self.filter(
            models.Q(serial_number__icontains=query or '') & models.Q(status__icontains=status or '')
        )


class StudentForms(models.Model):
    serial_number = models.CharField(max_length=120, unique=True)
    pin_code = models.CharField(max_length=120)
    form_type = models.ForeignKey(max_length=60, to=FormTypeChoicesModel, on_delete=models.CASCADE,
                                  related_name='forms')
    cost = models.IntegerField(null=True, blank=True, help_text='Current in Ghana Cedis')
    candidate_name = models.CharField(max_length=120, null=True, validators=(validate_alphanumberic_space,), blank=True)
    candidate_phone_number = PhoneNumberField(null=True, blank=True)
    sales_point = models.CharField(max_length=120, null=True, blank=True)
    sales_point_location = models.CharField(max_length=120, help_text='Town, city or community', null=True, blank=True)
    sales_agent = models.CharField(max_length=120, verbose_name='Sales agent\'s', null=True, blank=True)
    academic_year = models.CharField(max_length=10, help_text='this_year / next_year', null=True,
                                     choices=AcademicYear.choices(),
                                     default=AcademicYear.default(),
                                     blank=True
                                     )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=FormStatusChoice.choices, default=FormStatusChoice.NEW, null=True)
    is_current = models.BooleanField(default=True, help_text='Current status of the form.')
    objects = StudentFormsManager()

    class Meta:
        verbose_name_plural = 'Student Forms'
        permissions = [
            ('can_audit_admission_form', 'can audit student admission form'),
            ('can_reject_studentform', 'can reject student admission form'),
            ('can_accept_studentform', 'can accept student admission form'),
            ('view_studentform_detail', 'view student admission form detail'),
            ('view_own_forms', 'Can student view their own admission form detail'),
        ]

    def __str__(self):
        return 'Admission forms(%s)' % str(self.serial_number)

    @property
    def student(self):
        return self.student_admission_form

    @property
    def is_locked(self):
        return self.status in (FormStatusChoice.ACCEPTED, FormStatusChoice.REJECTED)

    @property
    def is_admitted(self):
        return self.status == FormStatusChoice.ACCEPTED

    @property
    def has_submitted(self):
        return self.status in (FormStatusChoice.SUBMITTED, FormStatusChoice.ACCEPTED)

    @property
    def can_edit(self):
        return not (self.has_submitted or self.is_locked)

    def get_absolute_url(self):
        return reverse('Admission:detail', kwargs={
            'serial_number': self.serial_number,
        })

    def get_absolute_update_url(self):
        return reverse('Admission:change', kwargs={
            'serial_number': self.serial_number,
            'id':self.id,
        })

    def get_absolute_student_form_url(self):
        return reverse('Admission:form_details',
                       kwargs={
                           'serial_number': self.serial_number,
                           'id':self.id
                       })


def auto_set_forms_status(instance, created, **kwargs):
    if created:
        instance.status = FormStatusChoice.NEW
        instance.save()


models.signals.post_save.connect(auto_set_forms_status, sender=StudentForms)


class SalesOfAdmissionForms(models.Model):
    identity = models.CharField(null=True, blank=True, help_text='ID.', max_length=120)
    admission_form = models.OneToOneField(StudentForms, on_delete=models.CASCADE, related_name='admission_form')
    received_from = models.CharField(max_length=120, help_text='payer\'s name')
    amount = models.FloatField(help_text='amount paying')
    the_sum_of = models.TextField(help_text='amount in words')
    timestamp = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=120)

    def __str__(self):
        return 'Sale of Admission forms ID:' + self.identity or self.id

    class Meta:
        verbose_name_plural = 'Sales of Admission Forms'


# todo create grade and their value model

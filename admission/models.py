from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from CollegeManagementSystem.validation import v_name

# class FormTypeChoiceManager(models.Manager):
#     def get_most_used(self):
#         return self.aggregate(models.Max())
#


class FormTypeChoicesModel(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title', 'id')

    def __str__(self):
        return self.title + ' (%s)' % self.subtitle


class FormStatusChoice(models.TextChoices):
    COMPLETED = 'completed', 'Completed'
    AT_PROFILE = 'at profile', 'At Profile'
    AT_ADDRESS = 'at address', 'At Address'
    AT_CERTIFICATION = 'at certification', 'At Certification'
    AT_EMPLOYMENT = 'at employment', 'At Employment History',
    AT_SPONSOR = 'at sponsor', 'AT SPONSORSHIP'
    AT_PROGRAMME = 'at programme', 'AT PROGRAMME'
    AT_EDUCATION = 'at education', 'AT EDUCATION'
    Expired = 'expired', 'Expired'
    NEW = 'new', 'New'


class StudentForms(models.Model):
    serial_number = models.CharField(max_length=120, unique=True)
    pin_code = models.CharField(max_length=120)
    form_type = models.ForeignKey(max_length=60, to=FormTypeChoicesModel, on_delete=models.CASCADE,
                                  related_name='form_type')
    cost = models.IntegerField(null=True, blank=True)
    candidate_name = models.CharField(max_length=120, null=True, validators=(v_name, ))
    candidate_phone_number = PhoneNumberField(null=True)
    sales_point = models.CharField(max_length=120, null=True)
    sales_point_location = models.CharField(max_length=120, help_text='Town, city or community', null=True)
    sales_agent = models.CharField(max_length=120, verbose_name='Sales agent\'s', null=True)
    academic_year = models.CharField(max_length=10, help_text='this_year / next_year', null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=30, choices=FormStatusChoice.choices, default=FormStatusChoice.NEW, null=True)

    class Meta:
        verbose_name_plural = 'Student Forms'


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

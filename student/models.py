from django.db import models

# Create your models here.
from accounts.models import User
from admission.models import StudentForms


class Student(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='student_profile')
    admission_form = models.OneToOneField(StudentForms, related_name='student_admission_form',
                                          on_delete=models.CASCADE, unique=True)

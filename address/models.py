from django.db import models
from django_countries.fields import CountryField
from CollegeManagementSystem.validation import validate_alphanumberic_space

from accounts.models import User


class Address(models.Model):
    country = CountryField(null=True, help_text="Country or Nationality")
    region = models.CharField(null=True, max_length=120, validators=(validate_alphanumberic_space,))
    district = models.CharField(null=True, max_length=120, validators=(validate_alphanumberic_space,))
    home_town = models.CharField(null=True, max_length=120, validators=(validate_alphanumberic_space,))
    address = models.CharField(null=True, max_length=120)
    current_region = models.CharField(null=True, max_length=120, validators=(validate_alphanumberic_space,))
    current_latitude = models.CharField(max_length=60, null=True, blank=True)
    current_longitude = models.CharField(max_length=60, null=True, blank=True)
    profile = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return str(self.address)

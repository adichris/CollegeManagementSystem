from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseUserManager
from CollegeManagementSystem.utilities import unique_slug_generate
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import user_logged_in, user_logged_out
from CollegeManagementSystem.validation import validate_alphanumberic_space
from django.contrib.sessions.models import Session
from django.shortcuts import reverse


class GenderChoices(models.TextChoices):
    MALE = ("m", "♂️ Male")
    FEMALE = ("f", "♀️ Female")
    TRANSGENDER = ("t", "⚧️ Transgender")
    OTHER = ("o", "Other ")


# class UserType(models.TextChoices):
#     ADMIN = ("admin", "Administrator")
#     FEMALE = ("superuser", "SuperUser")
#     TRANSGENDER = ("staff", "Staff")
#     OTHER = ("lecturer", "Lecturer")


def upload_user_to_path(instance, filename):
    import os
    unique = instance.id or instance.identity
    new_filename = str(unique) + os.path.splitext(filename)[-1]
    return os.path.join("user", "profile_picture", new_filename)


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password, identity, **kwargs):
        usr = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            identity=identity,
            **kwargs
        )

        usr.set_password(password)
        usr.save()
        return usr

    def create_superuser(self, first_name, last_name, email, password, phone_number, identity, **kwargs):
        usr = self.create_user(first_name, last_name, phone_number=phone_number, password=password, email=email, identity=identity, **kwargs)
        usr.is_superuser = True
        usr.save()
        return usr

    def search(self, query):
        qry = models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query)
        return self.filter(qry)


class User(PermissionsMixin, AbstractBaseUser):
    first_name = models.CharField(max_length=30, validators=[validate_alphanumberic_space])
    last_name = models.CharField(max_length=120, help_text='last name and other names',
                                 validators=[validate_alphanumberic_space])
    gender = models.CharField(max_length=5, choices=GenderChoices.choices, null=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(help_text='international phone number', unique=True)
    picture = models.ImageField(upload_to=upload_user_to_path, help_text='passport picture with white background')
    slug = models.SlugField(null=True, unique=True)
    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True) 
    identity = models.CharField(unique=True, null=True, max_length=30)
    session_key = models.CharField(max_length=100, unique=True, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']
    USERNAME_FIELD = 'identity'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    # browser information
    computer_name = models.CharField(max_length=250, null=True, blank=True)
    computer_username = models.CharField(max_length=250, null=True, blank=True)
    http_sec_ch_ua = models.CharField(max_length=250, null=True, blank=True)
    os = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        """Meta definition for User."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ("first_name", "last_name", "email")
        permissions = [
            ('can_view_profile', 'Can view their profile'),
            ('add_lecturerprofile', 'Add Lecturer Profile'),
            ('view_lecturerprofile', 'Can View Lecturer Profile'),
            ('set_password4other', 'Set password for other user'),
            ('self_change_password', 'Can user change his or her password'),
        ]

    def __str__(self):
        """Unicode representation of User."""
        return self.identity

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def get_department(self):
        if self.is_teaching_staff:
            return self.lecturer.department
        elif self.is_student:
            return self.student.programme.department
        return 'N/A'

    @property
    def student(self):
        try:
            return self.student_profile
        except models.ObjectDoesNotExist:
            return None

    @property
    def is_teaching_staff(self):
        try:
            return bool(self.lecturer)
        except models.ObjectDoesNotExist:
            return False

    def get_name_abr(self):
        f_abr = "".join([list(n)[0] for n in self.first_name.split(" ")]).upper()
        l_abr = "".join([list(n)[0] for n in self.last_name.split(" ")]).upper()
        return f_abr + l_abr

    @property
    def is_staff(self):
        return self.is_active and (self.is_superuser or self.is_admin)
    #
    # def has_perm(self, perm, obj=None):
    #     if self.is_superuser:
    #         return True
    #     return super(User, self).has_perm(perm, obj)

    def get_category(self):
        if self.student:
            return 'Student'
        elif self.is_admin and self.is_superuser:
            return 'Administrator and Superuser'
        elif self.is_admin:
            return 'Administrator'
        elif self.is_superuser:
            return 'Superuser'
        elif self.is_staff:
            return 'Staff'
        elif self.is_teaching_staff:
            return 'Lecturer'

    @property
    def is_student(self):
        try:
            student = self.student
            if student:
                return self.is_active and student.is_active
        except models.ObjectDoesNotExist or AttributeError:
            return False

    def get_absolute_url(self):
        return reverse('Student:home')


@receiver(models.signals.pre_save, sender=User)
def auto_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generate(instance)


@receiver(user_logged_in, sender=User)
def auto_show_user_online(sender, user, **kwargs):
    user.is_online = True
    user.save()


@receiver(user_logged_out, sender=User)
def auto_show_user_offline(sender, user=None, **kwargs):
    user.is_online = False
    user.save()


@receiver(models.signals.post_save, sender=User)
def auto_logout_user(sender, instance, **kwargs):
    if not instance.is_online:
        try:
            session = Session.objects.get(session_key=instance.session_key)
            session.delete()
        except Session.DoesNotExist:
            pass

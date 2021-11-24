from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseUserManager
from CollegeManagementSystem.utilities import unique_slug_generate
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import user_logged_in, user_logged_out
from CollegeManagementSystem.validation import validate_alphanumberic_space


class GenderChoices(models.TextChoices):
    MALE = ("m", "♂️ Male")
    FEMALE = ("f", "♀️ Female")
    TRANSGENDER = ("t", "⚧️ Transgender")
    OTHER = ("o", "Other ")


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
    first_name = models.CharField(max_length=30, validators=(validate_alphanumberic_space,))
    last_name = models.CharField(max_length=120, help_text='last name and other names', validators=(validate_alphanumberic_space,))
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

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']
    USERNAME_FIELD = 'identity'
    EMAIL_FIELD = 'email'
    objects = UserManager()
    
    class Meta:
        """Meta definition for User."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ("first_name", "last_name", "email")

    def __str__(self):
        """Unicode representation of User."""
        return self.get_full_name()

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def student(self):
        try:
            return self.student_profile
        except models.ObjectDoesNotExist:
            return None

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


@receiver(models.signals.pre_save, sender=User)
def auto_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generate(instance)


@receiver(user_logged_in, sender=User)
def auto_show_user_online(sender, user, **kwargs):
    user.is_online = True
    user.save()


@receiver(user_logged_out, sender=User)
def auto_show_user_online(sender, user=None, **kwargs):
    user.is_online = False
    user.save()

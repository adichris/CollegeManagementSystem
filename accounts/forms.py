from django import forms
from .models import User
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions


MINIMUM_USER_AGE = 10
PASSPORT_PICTURE_SIZE = (600, 600)


class UserCreationForm(forms.ModelForm):
    """Form definition for UserCreation."""
    password = forms.CharField(label="Password", max_length=16, required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Password comfirmation", max_length=16, required=True,
                                            widget=forms.PasswordInput)

    class Meta:
        """Meta definition for UserCreationform."""

        model = User
        fields = ('identity', 'first_name', 'last_name',
                  'gender', 'email', 'date_of_birth', 'phone_number')

    def clean_password_confirmation(self):
        pwd = self.cleaned_data.get("password")
        pwd_cfm = self.cleaned_data.get("password_confirmation")

        minimum_password_validator = MinimumLengthValidator(4)
        minimum_password_validator.validate(pwd_cfm)

        if pwd != pwd_cfm:
            raise forms.ValidationError("passwords does not match", code="invalid")

        return pwd_cfm

    def save(self, commit=True):
        instance = super().save(False)
        instance.set_password(self.clean_data["password"])
        if commit:
            instance.save()
        return instance


class UserProfileForm(forms.ModelForm):
    """Form definition for Users (student, staff, admin). profile"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'gender', 'email', 'date_of_birth', 'phone_number', 'picture')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={"type": "date"}),
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.add_input(Submit('save', 'Save Changes'))
        # helper.layout = Layout(
        #     Fieldset(
        #         'Personal Information'
        #     ),
        #     FormActions(
        #         Button('reset', 'Reset'),
        #         Submit('save', 'Save Changes'),
        #     )
        # )
        return helper

    def clean_picture(self):
        picture = self.cleaned_data["picture"]
        a, b = PASSPORT_PICTURE_SIZE
        file_size = a * b
        if picture.size > file_size :
            from django.template.defaultfilters import filesizeformat
            f_sizes = (filesizeformat(file_size), filesizeformat(picture.size))
            raise forms.ValidationError('Your passport picture picture size should be less than %. You uploaded %s ',
                                        f_sizes)
        # from PIL import Image
        # picture.image.resize(PASSPORT_PICTURE_SIZE, Image.ANTIALIAS)
        return picture

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        import datetime
        to_year = datetime.date.today().year
        student_age = to_year - dob.year
        student_year = dob.year
        if student_year >= to_year or student_age <= MINIMUM_USER_AGE:
            raise forms.ValidationError('You can not be %s years old. we are in %s' % (student_age, to_year))
        return dob


class UserChangeForm(forms.ModelForm):
    """Form definition for UserChange."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        """Meta definition for UserChangeform."""

        model = User
        fields = ('first_name', 'last_name', 'gender', 'email', 'date_of_birth', 'phone_number',
                  'password', 'is_active', 'is_admin', 'identity', 'picture')

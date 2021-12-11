from django import forms
from .models import Lecturer
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton, FormActions
from INSTITUTION.utils import file_size_validator, pdf_ext_validator

FILE_SIZE = (1800, 1800)


class LecturerCreationForm(forms.ModelForm):
    """Form definition for Lecturer."""

    class Meta:
        """Meta definition for LecturerCreationform."""

        model = Lecturer
        fields = ('identity', 'department', 'application_letter', 'cv')

    @property
    def helper(self):
        helper = FormHelper(self)

        return helper


class LecturerApplicationChangeForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('application_letter', 'cv')

    def __init__(self, *args, **kwargs):
        super(LecturerApplicationChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['accept'] = '.pdf'

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn-light shadow-sm'),
                StrictButton('Save Change', type='submit', css_class='btn-primary', onclick='dynamicSpinner(this)'),
                css_class='d-flex gap-3'
            )
        )
        return helper

    def clean_application_letter(self):
        app_letter = self.cleaned_data.get('application_letter')
        pdf_ext_validator(app_letter.name)
        file_size_validator(app_letter, FILE_SIZE)
        return app_letter

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        pdf_ext_validator(cv.name)
        file_size_validator(cv, FILE_SIZE)
        return cv


class DepartmentAssigmentForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('department', )

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton(
                    'Reset', type='reset', css_class='btn btn-light'
                ),
                StrictButton(
                    'Save', type='submit', css_class='btn btn-primary', onclick='dynamicSpinner(this)'
                ),
                css_class='d-flex justify-content-end'
            )
        )
        return helper


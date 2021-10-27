from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton, FormActions

from .models import Department


class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'short_form', 'faculty')

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

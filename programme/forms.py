from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton

from .models import Programme


class ProgrammeCreationForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ('name', 'department')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', type='submit', css_class='btn btn-primary'),
                css_class='d-flex justify-content-end'
            )
        )
        return helper

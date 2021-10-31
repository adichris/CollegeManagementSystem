from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton

from .models import Programme


class ProgrammeCreationForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ('name', 'department')

    def __init__(self, department_queryset=None, *args, **kwargs):
        super(ProgrammeCreationForm, self).__init__(*args, **kwargs)
        if department_queryset:
            self.fields['department'].queryset = department_queryset
            self.fields['department'].initial = department_queryset.first()

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', type='submit', css_class='btn btn-primary', onclick='dynamicSpinner(this)'),
                css_class='d-flex justify-content-end'
            )
        )
        return helper

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Reset

from .models import StudentSponsor


class StudentSponsorCreationForm(forms.ModelForm):
    class Meta:
        model = StudentSponsor
        exclude = ('student', )
        widgets = {
            'scholarship': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'on_government_support': forms.CheckboxInput(attrs={'type': 'checkbox'}),
        }

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.use_custom_control = True
        helper.form_method = 'POST'
        helper.layout.append(
            FormActions(Reset('reset', 'Reset'), Submit('save', 'Save'), css_class='d-flex justify-content-end gap-3')
        )
        return helper

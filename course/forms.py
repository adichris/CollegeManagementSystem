from django import forms
from .models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton, UneditableField
from crispy_forms.layout import Div


class DFlexDiv(Div):
    def __init__(self, *args, **kwargs):
        super(DFlexDiv, self).__init__(*args, **kwargs)


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'code', 'programme', 'semester', 'level', 'credit_hours', 'level', 'description')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn-light shadow-sm'),
                StrictButton('Save', type='submit', css_class='btn-primary shadow-sm'),
                css_class='d-flex justify-content-end',
            )
        )
        helper[:2].wrap_together(DFlexDiv, css_class='d-flex  gap-3', css_id='IDnameCode')
        return helper
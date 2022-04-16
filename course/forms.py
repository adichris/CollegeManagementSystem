from django import forms
from .models import Course, CourseAssignment
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton, UneditableField
from crispy_forms.layout import Div


class DFlexDiv(Div):
    def __init__(self, *args, **kwargs):
        super(DFlexDiv, self).__init__(*args, **kwargs)


def form_helper(self):
    helper = FormHelper(self)
    helper.layout.append(
        FormActions(
            StrictButton('Reset', type='reset', css_class='btn-light shadow-sm'),
            StrictButton('Save', type='submit', css_class='btn-primary shadow-sm', onclick='dynamicSpinner(this)'),
            css_class='d-flex justify-content-end',
        )
    )
    return helper


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'code', 'programme', 'semester', 'level', 'credit_hours', 'level', 'description')

    @property
    def helper(self):
        helper = form_helper(self)
        helper[:2].wrap_together(DFlexDiv, css_class='d-flex  gap-3', css_id='IDnameCode')
        return helper


class CourseFilter(forms.Form):
    name_start_with = forms.CharField(max_length=10, required=False)
    name = forms.CharField(max_length=10, required=False, help_text='Search by course name')
    course_code = forms.CharField(max_length=20, required=False,
                                  help_text='Course Code contains or similar.')
    programme_name = forms.CharField(required=False,
                                     help_text='Programme name like or contains. Search by programme name.')
    paginate_by = forms.CharField(required=False, help_text='Limit page number to.', widget=forms.NumberInput)

    @property
    def helper(self):
        helper = form_helper(self)
        helper[:2].wrap_together(DFlexDiv, css_class='d-flex  gap-3', css_id='IDnameCode')
        return helper


class CourseAssignmentForm(forms.ModelForm):
    class Meta:
        model = CourseAssignment
        fields = ('course', 'lecturer', 'is_tutor')

    @property
    def helper(self):
        helper = form_helper(self)
        helper[0].wrap_once(DFlexDiv, css_class='user-select-none')
        return helper

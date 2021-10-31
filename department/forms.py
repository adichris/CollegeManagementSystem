from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton, FormActions

from .models import Department


class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('faculty', 'name', 'short_form', 'picture')
        widgets = {
            'picture': forms.FileInput(attrs={
                'type': 'file'
            })
        }

    def __init__(self, faculty_queryset, *args, **kwargs):
        super(DepartmentCreationForm, self).__init__(*args, **kwargs)
        if faculty_queryset:
            self.fields['faculty'].queryset = faculty_queryset
            self.fields['faculty'].initial = faculty_queryset.first()

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


class DepartmentChangeForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('faculty', 'name', 'short_form', 'picture')

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

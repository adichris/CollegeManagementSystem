from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton

from .models import Student, StudentProgrammeChoice, CertExamRecord, StudentPreviousEducation


class ProgrammeSelectionChangeForm(forms.ModelForm):
    class Meta:
        model = StudentProgrammeChoice
        exclude = (
            'student',
        )

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', type='submit', css_class='btn btn-primary'),
                css_class='d-flex justify-content-end',
            )
        )
        return helper

    def clean_second_choice(self):
        programme2 = self.cleaned_data.get('second_choice')
        programme1 = self.cleaned_data.get('first_choice')
        if programme2 == programme1:
            raise forms.ValidationError('Your second choice must not be same as your first choice')

        return programme2

    def clean_third_choice(self):
        programme1 = self.cleaned_data.get('first_choice')
        programme2 = self.cleaned_data.get('second_choice')
        programme3 = self.cleaned_data.get('third_choice')
        if programme3 in (programme1, programme2):
            raise forms.ValidationError('Programmes selection must be unique.')
        return programme3


class CertExamRecordForm(forms.ModelForm):
    class Meta:
        model = CertExamRecord
        fields = (
            'examination_type',
            'examination_year',
            'school',
            'index_number',
            'subject',
            'grade',
        )
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "There are some duplications in your form.'s %(field_labels)s are not unique."
            }
        }

    def __init__(self, certificate_id,  *args, **kwargs):
        super(CertExamRecordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(**{'style': 'min-width:8em'})
        self.instance.certification_id = certificate_id

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', type='submit', css_class='btn btn-primary'),
                css_class='d-flex justify-content-end',
            )
        )
        return helper


class StudentPreviousEducationChangeForm(forms.ModelForm):
    class Meta:
        model = StudentPreviousEducation
        fields = ('school', 'region', 'from_year', 'to_year')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', type='submit', css_class='btn btn-primary'),
                css_class='d-flex justify-content-end',
            )
        )
        return helper

    def clean_to_year(self):
        to_year = self.cleaned_data.get('to_year')
        from_year = self.cleaned_data.get('from_year')
        if to_year <= from_year + 1:
            raise forms.ValidationError('The year you completed that school is invalid')
        return to_year

    def __init__(self, student_id, *args, **kwargs):
        super(StudentPreviousEducationChangeForm, self).__init__(*args, **kwargs)
        self.instance.student_id = student_id


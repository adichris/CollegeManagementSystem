from .models import Student, StudentProgrammeChoice, CertExamRecord
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton


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

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', type='submit', css_class='btn btn-primary'),
                css_class='d-flex justify-content-center',
            )
        )
        return helper

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton, FormActions, UneditableField
from crispy_forms.layout import HTML, Div

from .models import Faculty


class FacultyCreationForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ('slug', )
        widgets = {
            'picture': forms.FileInput(attrs={'type': 'file'}),
            'icon': forms.FileInput(attrs={'type': 'file'}),
        }

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_method = 'POST'
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', css_class='btn btn-primary', type='submit'),
                css_class='d-flex justify-content-end'
            )
        )

        return helper


class FacultyChangeForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'icon', 'picture', 'note')
        model = Faculty

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_method = 'POST'
        helper['slug'].wrap(UneditableField)
        helper.layout.append(
            FormActions(
                Div(css_id='repalceWBtn')
                ,
                Div(
                StrictButton('Reset', type='reset', css_class='btn btn-light'),
                StrictButton('Save', css_class='btn btn-primary', type='submit'),
                    css_class='align-self-end', css_id='resetBtn'
                ),
            )
        )

        return helper



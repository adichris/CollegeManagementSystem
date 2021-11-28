from .models import SemesterModel, Level
from django import forms
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import StrictButton, FormActions
from django.contrib.auth.models import Group


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', )

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn-light'),
                StrictButton('Save', type='submit', onlcick='dynamicSpinner(this)', css_class='btn-primary'),
                css_class='d-flex justify-content-end gap-3'
            )
        )
        helper[0].wrap_together(FloatingField)
        return helper


class SemesterCreationForm(forms.ModelForm):
    class Meta:
        model = SemesterModel
        fields = ('name', 'is_current')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn-light'),
                StrictButton('Save', type='submit', onlcick='dynamicSpinner(this)', css_class='btn-primary'),
                css_class='d-flex justify-content-end gap-3'
            )
        )
        helper[0].wrap_together(FloatingField)
        return helper

    def clean_is_current(self):
        is_current = self.cleaned_data.get('is_current')

        if is_current:
            query = self.Meta.model.objects.filter(is_current=is_current)
            if query.exists():
                raise forms.ValidationError('There is a semester marked as Current please change that first.')
        return is_current


class LevelCreationForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = '__all__'

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn-light'),
                StrictButton('Save', type='submit', onlcick='dynamicSpinner(this)', css_class='btn-primary', name='save_level'),
                css_class='d-flex justify-content-end gap-3'
            )
        )

        helper[0].wrap_together(FloatingField)
        return helper

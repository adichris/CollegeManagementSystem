from django import forms
from .models import EmploymentHistoryModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset
from crispy_forms.bootstrap import FormActions, AccordionGroup


class EmploymentHistoryCreationForm(forms.ModelForm):
    class Meta:
        fields = (
            'has_history', 'job_title', 'specific_duty',
            'supervisor', 'company_name', 'address',
            'city', 'state', 'employed_from', 'employed_to', 'why_leave'
        )
        model = EmploymentHistoryModel
        widgets = {
            'has_history': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'employed_to': forms.DateInput(attrs={'type': 'date'}),
            'employed_from': forms.DateInput(attrs={'type': 'date'}),
        }

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.use_custom_control = True
        helper.layout.append(
            FormActions(Reset('reset', 'Reset'), Submit('save', 'Save'),
                        css_class='d-flex justify-content-end gap-3 my-3')
        )
        helper[1:len(self.fields)].wrap_together(
            EHAccordionGroup,
        )
        helper.form.novalidate = True
        return helper

    # def clean_has_history(self):
    #     has_hist = self.cleaned_data.get('has_history')
    #     has_data = self.cleaned_data.get('company_name') or self.cleaned_data.get('employed_from') or self.cleaned_data.get('why_leave')
    #     if has_hist and not has_data:
    #         raise forms.ValidationError('You need to provide us details of your employment history')
    #     if not has_hist and has_data:
    #         raise forms.ValidationError('Clear all entries before you uncheck this*')
    #
    #     return has_hist

    def clean_address(self):
        has_hist = self.cleaned_data.get('has_history')
        address = self.cleaned_data.get('address')

        if has_hist and not address:
            raise forms.ValidationError('Address is required')

        return address

    def clean_city(self):
        has_hist = self.cleaned_data.get('has_history')
        city = self.cleaned_data.get('city')

        if has_hist and not city:
            raise forms.ValidationError('In what city?')

        return city

    def clean_company_name(self):
        has_hist = self.cleaned_data.get('has_history')
        company_name = self.cleaned_data.get('company_name')

        if has_hist and not company_name:
            raise forms.ValidationError('Please enter the company name')
        return company_name

    def clean_employed_from(self):
        has_hist = self.cleaned_data.get('has_history')
        employed_from = self.cleaned_data.get('employed_from')

        if has_hist and not employed_from:
            raise forms.ValidationError('Date you got employ is required')
        return employed_from

    def clean_employed_to(self):
        has_hist = self.cleaned_data.get('has_history')
        employed_to = self.cleaned_data.get('employed_to')

        if has_hist and not employed_to:
            raise forms.ValidationError('This field is required')
        return employed_to

    def clean_job_title(self):
        has_hist = self.cleaned_data.get('has_history')
        job_title = self.cleaned_data.get('job_title')

        if has_hist and not job_title:
            raise forms.ValidationError('This is required')
        return job_title


class EHAccordionGroup(AccordionGroup):
    def __init__(self, *args, **kwargs):
        super(EHAccordionGroup, self).__init__('Add Employment History', *args, css_id='id_EHist', **kwargs)

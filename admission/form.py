from django import forms
from .models import StudentForms, AcademicYear, FormTypeChoicesModel
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.layout import Div
from CollegeManagementSystem.validation import validate_alphanumberic_space


class AdmissionLoginForm(forms.Form):
    serial_number = forms.CharField(max_length=120)
    pin_code = forms.CharField(max_length=120, widget=forms.PasswordInput)


class StudentFormsCreation(forms.ModelForm):
    class Meta:
        model = StudentForms
        fields = ('serial_number', 'pin_code', 'academic_year', 'form_type')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset'),
                StrictButton('Save', type='submit', css_class='btn-primary'),
                css_class='d-flex justify-content-end'
            )
        )
        return helper


class StudentFormsChange(forms.ModelForm):
    class Meta:
        model = StudentForms
        exclude = ('status', )

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset'),
                StrictButton('Save', type='submit', css_class='btn-primary'),
                css_class='d-flex justify-content-end'
            )
        )
        return helper


class AdmissionFromBatchCreation(forms.Form):
    quantity = forms.IntegerField(help_text='Number of forms to create.', max_value=500, required=True, initial=1)
    characters = forms.IntegerField(help_text='Number of characters per serial number', initial=8, max_value=20)
    pin_code_length = forms.IntegerField(initial=8, help_text='Number of Character to form Pin code', max_value=20)
    academic_year = forms.ChoiceField(choices=AcademicYear.choices(), initial=AcademicYear.default(),
                                      help_text='Academic year for the admission form')
    form_type = forms.ModelChoiceField(FormTypeChoicesModel.objects.get_for_form_batch_creation())
    prefix = forms.CharField(required=False, help_text='Append to the serial number. Eg append+serial_number',
                             label='Prefix (Optional)', initial='SN', validators=[validate_alphanumberic_space], max_length=15)
    suffix = forms.CharField(required=False, help_text='Prepend to serial number. Eg serial_number+suffix',
                             label='Suffix (Optional)', validators=[validate_alphanumberic_space], max_length=15)
    cost = forms.IntegerField(help_text='Cost of each form in Ghana Cedis (GHc)', label='Cost (optional)',
                              required=False)

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset'),
                StrictButton('Preview', type='button', css_class='btn-outline-primary', onclick='dynamicSpinner(this)'),
                StrictButton('Generate', type='submit', css_class='btn-primary', onclick='dynamicSpinner(this)'),
                css_class='d-flex justify-content-end'
            )
        )
        helper[:2].wrap_together(Div, css_class='d-flex flex-column flex-md-row gap-3')
        helper[1:3].wrap_together(Div, css_class='d-flex flex-column flex-md-row gap-3')
        helper[3:5].wrap_together(Div, css_class='d-flex flex-column flex-md-row gap-3')
        helper.all().update_attributes(css_class='flex-grow-1')
        return helper

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty < 1:
            raise forms.ValidationError('The minimum value must be 1')
        elif qty > 500:
            raise forms.ValidationError('The maximum value must be 500')

        return qty

    def clean_characters(self):
        characters = self.cleaned_data.get('characters')
        if characters < 4:
            raise forms.ValidationError('Minimum characters length must be 4')
        elif characters > 20:
            raise forms.ValidationError('Maximum characters length must be 20')
        return characters

    def clean_pin_code_length(self):
        pin_code_length = self.cleaned_data.get('pin_code_length')
        if pin_code_length < 4:
            raise forms.ValidationError('The minimum pin code characters length must be 4')
        elif pin_code_length > 20:
            raise forms.ValidationError('The maximum pin code characters length must be 4')
        return pin_code_length

    def clean_prefix(self):
        prefix = self.cleaned_data.get('prefix')
        if len(prefix) > 16:
            raise forms.ValidationError('Prefix is too long')
        return prefix

    def clean_suffix(self):
        suffix = self.cleaned_data.get('suffix')
        if len(suffix) > 16:
            raise forms.ValidationError('suffix is too long')
        return suffix


class FormTypeChoicesModelCreationForm(forms.ModelForm):
    class Meta:
        model = FormTypeChoicesModel
        fields = ('title', 'subtitle')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset'),
                StrictButton('Save', type='submit', css_class='btn-primary'),
                css_class='d-flex justify-content-end'
            )
        )
        return helper

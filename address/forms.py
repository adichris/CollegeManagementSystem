from django import forms
from .models import Address
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Reset, Submit


class AddressCreationForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('profile', 'current_latitude', 'current_longitude')

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.use_custom_control = True
        helper.layout.append(
            FormActions(Reset('reset', 'Reset'), Submit('save', 'Save'), css_class='d-flex justify-content-end gap-3')
        )
        return helper

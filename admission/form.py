from django import forms


class AdmissionLoginForm(forms.Form):
    serial_number = forms.CharField(max_length=120)
    pin_code = forms.CharField(max_length=120)

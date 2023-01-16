import datetime

from django import forms
from django.forms import ModelForm, DateInput

from apps.accounts.models import  Account



class CreateApartments(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ),
        help_text='İsim alanı en fazla 50 karakter olmalıdır ve zorunludur.',
        max_length=50,
        required=True,
    )


    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ),
        max_length=100,
        required=True,
    )



    class Meta:
        model = Account
        fields = ('name', 'address')


        def __init__(self):
            self.cleaned_data = None

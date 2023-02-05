import datetime

from django import forms
from django.forms import ModelForm, DateInput

from apps.accounts.models import Account



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


class CreateCustomerForm(forms.ModelForm):
    site_name = forms.CharField(
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

    tax_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "id":"tax_number",
                "placeholder": "",
                "class": "form-control",
                'oninput': 'limit_input_tax_number()'
            }
        ),
        max_length=10,
        required=True,
    )

    related_person_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ),
        max_length=50,
        required=True,
    )

    site_phone1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'oninput': 'limit_input_tax_number()'
            }
        ),
        max_length=11,
        required=True,
    )

    site_address = forms.CharField(
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
        fields = ('site_name', 'tax_number', 'related_person_name', 'site_phone1', "site_address", "licence_date")
        widgets = {
            'licence_date': DateInput(),
        }

        def __init__(self):
            self.cleaned_data = None

    def clean_site_name(self):
        site_name = self.cleaned_data['site_name']
        if Account.objects.filter(site_name=site_name).exists():
            raise forms.ValidationError("Bu site adı kullanılıyor.")
        return site_name

    def clean_tax_number(self):
        tax_number = self.cleaned_data['tax_number']

        if Account.objects.filter(tax_number=tax_number).exists():
            raise forms.ValidationError("Bu Vergi No kullanılıyor")
        return tax_number

    def clean_licence_date(self):
        licence_date = self.cleaned_data['licence_date']

        if licence_date < datetime.datetime.now():
            raise forms.ValidationError("Tarih bugünden eski olamaz")
        return licence_date
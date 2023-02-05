import datetime

from django import forms
from django.forms import ModelForm

from apps.accounts.models import  Account


class DateInput(forms.DateInput):
    input_type = 'date'


class EditCustomerForm(ModelForm):
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

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'oninput': 'limit_input_phone()'
            }
        ),
        max_length=11,
        required=True,
    )

    class Meta:
        model = Account
        fields = ('name', 'phone', "licence_date")
        widgets = {
            'licence_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.cleaned_data = None
        super(EditCustomerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['site_name'].widget.attrs['readonly'] = True

        # if check_something():
        #     self.fields['receive_newsletter'].initial = True

    def clean_site_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.site_name
        else:
            return self.cleaned_data['site_name']

    # def clean_licence_date(self):
    #
    #     licence_date = self.cleaned_data['licence_date']
    #
    #     if licence_date < datetime.datetime.now():
    #         raise forms.ValidationError("Tarih bugünden eski olamaz")
    #     return licence_date


class CreateCustomerForm(forms.ModelForm):
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



    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control",
                'oninput': 'limit_input_phone()'
            }
        ),
        max_length=11,
        required=True,
    )




    class Meta:
        model = Account
        fields = ('name', 'phone', "licence_date")
        widgets = {
            'licence_date': DateInput(),
        }

        def __init__(self):
            self.cleaned_data = None

    def clean_site_name(self):
        name = self.cleaned_data['name']
        if Account.objects.filter(name=name).exists():
            raise forms.ValidationError("Bu site adı kullanılıyor.")
        return name


    def clean_licence_date(self):
        licence_date = self.cleaned_data['licence_date']

        if licence_date < datetime.datetime.now():
            raise forms.ValidationError("Tarih bugünden eski olamaz")
        return licence_date




#from django.forms.fields import DateField
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms import widgets 
from .models import PlatformUsers, Address, Country, Industry_Type

from django import forms 
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
#from captcha.fields import CaptchaField
from django.contrib.auth.models import User
#import datetime


class UserCreationForm(UserCreationForm):
    username = forms.RegexField(
        label=("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=("Required. 30 characters or fewer. Letters, digits and "
                "@/./+/-/_ only."),
        error_messages={
        'invalid': ("This value may contain only letters, numbers and "
                     "@/./+/-/_ characters.")},
        widget=forms.TextInput(attrs={'class': 'form-control',
                            'required': 'true',
                            'placeholder': 'Username'
        })
        )
    #captcha = CaptchaField()
    
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class PlatformUsersForm(forms.ModelForm):

    class Meta:
        model = PlatformUsers
        fields = ['industry', 'phone_mobile_country', 'phone_mobile_number','phone_landline_country', 'phone_landline_number', 'company_name', 'company_position']


class AddressCountryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_simple_name()

class AddressForm(forms.ModelForm):
    country = AddressCountryModelChoiceField(required=True, queryset=Country.objects.all())

    class Meta:
        model = Address
        fields = ['street_address', 'city', 'region', 'zipcode', 'country']

        def __init__(self, *args, **kwargs):
            kwargs.setdefault('label_suffix', '')
            super(AddressForm, self).__init__(*args, **kwargs)


class DateInput(forms.DateInput):
    input_type = 'date'


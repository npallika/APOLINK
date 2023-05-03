from django.forms import widgets 
from .models import PlatformUsersAll
from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class UserCreationForm(UserCreationForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                "@/./+/-/_ only."),
        error_messages={
        'invalid': _("This value may contain only letters, numbers and "
                     "@/./+/-/_ characters.")},
        widget=forms.TextInput(attrs={'class': 'form-control',
                            'required': 'true',
                            'placeholder': 'Username'
        })
        )
    #captcha = CaptchaField()
    #password = forms.CharField(widget=forms.PasswordInput())
    
    # Possible implementation: Only show password fields when creating a new user
    '''
    def __init__(self, *args, **kwargs):
        update = kwargs.pop('update', False)
        super().__init__(*args, **kwargs)
        if update:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields.pop('password1')
            self.fields.pop('password2')    
    '''  
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels= {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email address'),
            'password1': _('Password'),
            'password2': _('Password confirmation'),
        }


# you have to create another form for updating, just because you don't want to update passwords with form system, but with django password system
class UserUpdateForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
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
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
        labels = {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),}


#Is not used : i preferred to use just directly the AuthenticationForm in views, but useful for moving the complexity to forms.py
class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_active:
            login(self.request, user)
            messages.success(self.request, _('You have successfully logged in')) 
        else:
         messages.warning(self.request, _('Your account is not active.'))


class AddressCountryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_simple_name()


class DateInput(forms.DateInput):
    input_type = 'date'


# Unique Form with Address and Users information
class PlatformUsersFormAll(forms.ModelForm):

    class Meta:
        model = PlatformUsersAll
        fields = ['industry', 'phone_mobile_country', 'phone_mobile_number','phone_landline_country', 'phone_landline_number', 'company_name', 'company_position','street_address', 'city', 'region', 'zipcode', 'country']
        labels= {
            'industry': _('industry'),
            'phone_mobile_country': _('phone mobile country'),
            'phone_mobile_number': _('phone mobile number'),
            'phone_landline_country': _('phone landline country'),
            'phone_landline_number': _('phone landline number'),
            'company_name': _('company name'),
            'company_position': _('company position'),
            'street_address': _('street address'),
            'city': _('city'),
            'region': _('region'),
            'zipcode': _('zipcode'),
            'country': _('country'),
        }
        
        #probabily it is useful, in any case i need to let it to make some changes more in the future
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('label_suffix', '')
            super(PlatformUsersFormAll, self).__init__(*args, **kwargs)


#OLD IMPLEMENTATION : 2 different forms related to 2 different models
'''
class AddressForm(forms.ModelForm):
    country = AddressCountryModelChoiceField(required=True, queryset=Country.objects.all())

    class Meta:
        model = Address
        fields = ['street_address', 'city', 'region', 'zipcode', 'country']

        def __init__(self, *args, **kwargs):
            kwargs.setdefault('label_suffix', '')
            super(AddressForm, self).__init__(*args, **kwargs)
'''
'''
class PlatformUsersForm(forms.ModelForm):

    class Meta:
        model = PlatformUsers
        fields = ['industry', 'phone_mobile_country', 'phone_mobile_number','phone_landline_country', 'phone_landline_number', 'company_name', 'company_position']
'''
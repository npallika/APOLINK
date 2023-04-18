from modeltranslation.translator import register, TranslationOptions
from .models import Country, Industry_Type, PlatformUsersAll
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('code', 'phoneCode', 'name')

@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('username', 'first_name', 'last_name', 'email')

@register(Industry_Type)
class Industry_TypeTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(PlatformUsersAll)
class PlatformUsersAllTranslationOptions(TranslationOptions):
    fields = ('user', 'company_name', 'industry', 'company_position', 
              'phone_landline_country', 'phone_landline_number', 'phone_mobile_country',
              'phone_mobile_number',
              'street_address', 'city', 'region', 'zipcode', )



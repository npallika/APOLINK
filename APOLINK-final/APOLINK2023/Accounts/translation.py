from modeltranslation.translator import register, TranslationOptions
from .models import Country, Industry_Type, PlatformUsersAll
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )
    
'''
@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('username', 'first_name', 'last_name', 'email')
'''
@register(Industry_Type)
class Industry_TypeTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(PlatformUsersAll)
class PlatformUsersAllTranslationOptions(TranslationOptions):
    fields = () #check : industry (industry_type) , country (country name)



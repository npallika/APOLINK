from modeltranslation.translator import register, TranslationOptions
from .models import Country, Industry_Type, PlatformUsersAll
from django.utils.translation import gettext_lazy as _

#for every model you want to create translation fields : ModelName + TranslationOptions (TranslationOptions) and add fields to have fieldName_en / fieldName_el
@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )
    
@register(Industry_Type)
class Industry_TypeTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(PlatformUsersAll)
class PlatformUsersAllTranslationOptions(TranslationOptions):
    fields = ()


#just if you want to add translation fields for User
'''
@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('username', 'first_name', 'last_name', 'email')
'''


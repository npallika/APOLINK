from modeltranslation.translator import register, TranslationOptions
from .models import FirstLevelCategories, SecondLevelCategories
from django.utils.translation import gettext_lazy as _

@register(FirstLevelCategories)
class FirstLevelCategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'short_name',)

@register(SecondLevelCategories)
class SecondLevelCategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'short_name',)
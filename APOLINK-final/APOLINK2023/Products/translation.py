from modeltranslation.translator import register, TranslationOptions
from .models import ThirdLevelCategories
from django.utils.translation import gettext_lazy as _

@register(ThirdLevelCategories)
class ThirdLevelCategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'short_name',)
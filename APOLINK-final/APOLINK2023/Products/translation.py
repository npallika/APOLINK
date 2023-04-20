from modeltranslation.translator import register, TranslationOptions
from .models import *
from django.utils.translation import gettext_lazy as _

@register(ThirdLevelCategories)
class ThirdLevelCategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'short_name',)
    
@register(ProductsDisplayed)
class ProductsDisplayedTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_category', )
    
@register(ProductPhotos)
class ProductPhotosTranslationOptions(TranslationOptions):
    fields = ('photo','product', )

@register(CaseSealerSpecs)
class CaseSealerSpecsTranslationOptions(TranslationOptions):
    fields = ()

@register(CasePackerSpecs)
class CasePackerSpecsTranslationOptions(TranslationOptions):
    fields = ()

@register(DispersersSpecs)
class DispersersSpecsTranslationOptions(TranslationOptions):
    fields = ()

@register(PalletizerSpecs)
class PalletizerSpecsTranslationOptions(TranslationOptions):
    fields = ()

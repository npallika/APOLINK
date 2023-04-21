from modeltranslation.translator import register, TranslationOptions
from .models import *
from django.utils.translation import gettext_lazy as _

@register(ThirdLevelCategories)
class ThirdLevelCategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'short_name',)
    
@register(ProductsDisplayed)
class ProductsDisplayedTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_short_description', 'manufacturer', 'model',) #product category = foreign key
    
@register(ProductPhotos)
class ProductPhotosTranslationOptions(TranslationOptions):
    fields = () # don't need photo 

@register(CaseSealerSpecs)
class CaseSealerSpecsTranslationOptions(TranslationOptions):
    fields = ('type', )

@register(CasePackerSpecs)
class CasePackerSpecsTranslationOptions(TranslationOptions):
    fields = ('type', )

@register(DispersersSpecs)
class DispersersSpecsTranslationOptions(TranslationOptions):
    fields = ('type', 'application', )

@register(PalletizerSpecs)
class PalletizerSpecsTranslationOptions(TranslationOptions):
    fields = ('type', 'application',)

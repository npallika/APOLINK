from django.contrib import admin
from . import models
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class ThirdLevelCategoriesAdmin(TranslationAdmin):
    model = models.ThirdLevelCategories
    
class ProductsDisplayedAdmin(TranslationAdmin):
    model = models.ProductsDisplayed
    
class ProductPhotosAdmin(TranslationAdmin):
    model = models.ProductPhotos
    
class CaseSealerSpecsAdmin(TranslationAdmin):
    model = models.CaseSealerSpecs

class CasePackerSpecsAdmin(TranslationAdmin):
    model = models.CasePackerSpecs

class DispersersSpecsAdmin(TranslationAdmin):
    model = models.DispersersSpecs

class PalletizerSpecsAdmin(TranslationAdmin):
    model = models.PalletizerSpecs

# Register your models here.
admin.site.register(models.ProductPhotos, ProductPhotosAdmin)
admin.site.register(models.ThirdLevelCategories, ThirdLevelCategoriesAdmin)
admin.site.register(models.CaseSealerSpecs, CaseSealerSpecsAdmin)
admin.site.register(models.CasePackerSpecs, CasePackerSpecsAdmin)
admin.site.register(models.ProductsDisplayed, ProductsDisplayedAdmin)
admin.site.register(models.DispersersSpecs, DispersersSpecsAdmin)
admin.site.register(models.PalletizerSpecs, PalletizerSpecsAdmin)
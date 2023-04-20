from django.contrib import admin
from . import models
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class ThirdLevelCategoriesAdmin(TranslationAdmin):
    model = models.ThirdLevelCategories

# Register your models here.
admin.site.register(models.ProductPhotos)
admin.site.register(models.ThirdLevelCategories)
admin.site.register(models.CaseSealerSpecs)
admin.site.register(models.CasePackerSpecs)
admin.site.register(models.ProductsDisplayed)

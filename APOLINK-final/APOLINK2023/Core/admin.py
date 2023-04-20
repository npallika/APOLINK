from django.contrib import admin
from Core.models import *
from Products.models import *
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

# Register your models here.

class CategoriesInLine(admin.StackedInline):
    model = SecondLevelCategories
    extra = 0

class CategoriesAdmin(TranslationAdmin): #TranlationAdmin is a subclass of admin.ModelAdmin
    inlines = [CategoriesInLine]


admin.site.register(FirstLevelCategories, CategoriesAdmin)
#admin.site.register(models.SecondLevelCategories)
#admin.site.register(models.ThirdLevelCategories)

class SecondLevelCategoriesInLine(admin.StackedInline):
    model = ThirdLevelCategories
    extra = 0

class SecondLevelCategoriesAdmin(TranslationAdmin):
    inlines =[SecondLevelCategoriesInLine]

admin.site.register(SecondLevelCategories, SecondLevelCategoriesAdmin)
from django.contrib import admin
from . import models
from modeltranslation.admin import TranslationAdmin

#TRANSLATION WITH DJANGO MODEL TRANSLATION
class CountryAdmin(TranslationAdmin):
    model = models.Country

class PlatformUsersAllAdmin(TranslationAdmin):
    model = models.PlatformUsersAll
    
class Industry_TypeAdmin(TranslationAdmin):
    model = models.Industry_Type
  
'''
class UserAdmin(TranslationAdmin):
    model = User
'''

'''
class PlatformUsersAllInline(TranslationTabularInline):
    model = PlatformUsersAll


class CustomUserAdmin(UserAdmin, TranslationAdmin):
    inlines = [PlatformUsersAllInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
'''


# Register your models here.
admin.site.register(models.Country, CountryAdmin) #to delete translation : delete CountryAdmin class and ref.
admin.site.register(models.PlatformUsersAll, PlatformUsersAllAdmin)
#admin.site.register(models.Address)
admin.site.register(models.Industry_Type, Industry_TypeAdmin)
#admin.site.unregister(models.User)
#admin.site.register(models.User, UserAdmin)

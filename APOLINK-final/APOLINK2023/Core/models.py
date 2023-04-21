from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class FirstLevelCategories(models.Model):
    name = models.CharField(_('name'), max_length=200, null=True)
    short_name = models.CharField(_('short name'), max_length=40, null=True, blank=True)
    short_description = models.TextField(_('short description'),null=True, blank=True)
    slug = models.SlugField(_('slug'), allow_unicode=True, unique=True)
    icon = models.ImageField(upload_to='Core/Static/Photos/FirstLevelCategories', verbose_name=_("icon"), null=True, blank=True)
    class Meta:
        verbose_name = _("First Level Category")
        verbose_name_plural = _("First Level Categories")
    
    def __str__(self):
        return self.name + "( ID :" + str(self.id) +" )"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)    

class SecondLevelCategories(models.Model):
    name = models.CharField(_('name'), max_length=200, null=True)
    parent_cat = models.ForeignKey(FirstLevelCategories , verbose_name=_('parent category'), on_delete=models.CASCADE)
    short_name = models.CharField(_('short name'),max_length=40, null=True, blank=True)
    short_description = models.TextField(_('short description'),null=True, blank=True)
    slug = models.SlugField(_('slug'), allow_unicode=True, unique=True)
    icon = models.ImageField(upload_to='Core/Static/Photos/SecondLevelCategories',verbose_name=_("icon"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Second Level Category")
        verbose_name_plural = _("Second Level Categories")

    def __str__(self):
        return self.name + "( ID :" + str(self.id) +" )"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


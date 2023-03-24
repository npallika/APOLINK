from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class FirstLevelCategories(models.Model):
    name = models.CharField(max_length=200, null=True)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    icon = models.ImageField(upload_to='Core/Static/Photos/FirstLevelCategories', null=True, blank=True)
    
    
    def __str__(self):
        return self.name + "( ID :" + str(self.id) +" )"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)    

class SecondLevelCategories(models.Model):
    name = models.CharField(max_length=200, null=True)
    parent_cat = models.ForeignKey(FirstLevelCategories, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    icon = models.ImageField(upload_to='Core/Static/Photos/SecondLevelCategories', null=True, blank=True)
    
    def __str__(self):
        return self.name + "( ID :" + str(self.id) +" )"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


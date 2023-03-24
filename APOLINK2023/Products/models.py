from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


#  ------------------ Around Products --------------------------- #
class ThirdLevelCategories(models.Model):
    name = models.CharField(max_length=200, null=True)
    parent_cat = models.ForeignKey('Core.SecondLevelCategories', on_delete=models.CASCADE)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    icon = models.ImageField(upload_to='Core/Static/Photos/ThirdLevelCategories', null=True, blank=True)
    

    def __str__(self):
        return self.name + "( ID :" + str(self.id) +" )"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class ProductsDisplayed(models.Model):
    CHOICES = {
        ('Selling',"For Selling"),
        ('Renting',"For Renting"),
        ('Selling or Renting',"For Selling or Renting")
    }
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_registered = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
    manufactured_date = models.DateField(null=True)
    product_name = models.CharField(max_length=200,null=False)
    product_category = models.ForeignKey(ThirdLevelCategories, null=True, on_delete=models.CASCADE)
    product_short_description = models.TextField(null=True, blank=True)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    for_sell_rent = models.CharField(verbose_name="For sell, rent or both", max_length=40, choices=CHOICES, blank=True, null=True)
    model = models.CharField(max_length=200, null=True, blank=True)
   
    class Meta:
        verbose_name = 'Product Displayed'
        verbose_name_plural = 'Products Displayed'
           
    def __str__(self):
        return self.product_name

   
class ProductPhotos(models.Model):
    #photo_name = models.CharField(max_length=200, null=False)
    photo = models.ImageField(upload_to ='upload/', null=True, blank=True)
    product = models.ForeignKey(ProductsDisplayed, null=True,  on_delete=models.CASCADE)
    #default = models.BooleanField(default=False)

    '''def __str__(self):
        return self.photo_name'''

#  ------------------ Around Specifications --------------------------- #

class CaseSealerSpecs(models.Model):
    TYPES = (
        ('BtmDr', 'Bottom Driven'),
        ('SdDr', 'Side Driven'),
        ('T&BtmDr', 'Top & Bottom Driven')
    )
    product = models.OneToOneField(ProductsDisplayed, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Case Sealer Type", max_length=25, choices=TYPES, blank=True, null=True)
    min_box_size_cm = models.PositiveIntegerField(verbose_name="Minimum Box Size (cm)", default=10, validators=[MinValueValidator(1), MaxValueValidator(20)])
    max_box_size_cm = models.PositiveIntegerField(verbose_name="Maximum Box Size (cm)", default=20, validators=[MinValueValidator(1), MaxValueValidator(100)])
    boxes_per_min = models.PositiveIntegerField(verbose_name="Maximum boxes per min", default=5, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.product.id}. {self.product.product_name} specs"

class CasePackerSpecs(models.Model):
    TYPES = (
        ('top', 'Top Loader'),
        ('side', 'Side Loader'),
        ('P&PL', 'Pick and Place')
    )
    product = models.OneToOneField(ProductsDisplayed, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Case Packer Type", max_length=25, choices=TYPES, blank=True, null=True)
    boxes_per_min = models.PositiveIntegerField(verbose_name="Maximum boxes per min", default=5, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    def __str__(self):
        return f"{self.product.id}. {self.product.product_name} specs"
    

class DispersersSpecs(models.Model):
    TYPES = (
        ('batch', 'Batch'),
        ('continuous', 'Continuous')
    )
    product = models.OneToOneField(ProductsDisplayed, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Batch/Continuous", max_length=25, choices=TYPES, blank=True, null=True)
    power = models.FloatField(verbose_name="Motor Power in kW")
    application = models.CharField(verbose_name="Application", max_length=80, blank=True, null=True)


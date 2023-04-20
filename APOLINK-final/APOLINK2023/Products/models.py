from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


#  ------------------ Around Products --------------------------- #
class ThirdLevelCategories(models.Model):
    name = models.CharField(_('name'),max_length=200, null=True)
    parent_cat = models.ForeignKey('Core.SecondLevelCategories', verbose_name=_('parent cat'), on_delete=models.CASCADE)
    short_name = models.CharField(_('short name'), max_length=40, null=True, blank=True)
    short_description = models.TextField(_('short description'), null=True, blank=True)
    slug = models.SlugField(_('slug'), allow_unicode=True, unique=True)
    icon = models.ImageField(_('icon'),upload_to='Core/Static/Photos/ThirdLevelCategories', null=True, blank=True)
    
    class Meta:
        verbose_name = _("Third Level Category")
        verbose_name_plural = _("Third Level Categories")
        
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
    user = models.ForeignKey(User, verbose_name=_('user'), null=True, blank=True, on_delete=models.CASCADE)
    date_registered = models.DateField(verbose_name=_('date registered'), default=timezone.now)
    date_updated = models.DateField(verbose_name=_('date updated'), auto_now=True)
    manufactured_date = models.DateField(verbose_name=_('manufactered_date'),null=True)
    product_name = models.CharField(_('product name'), max_length=200,null=False)
    product_category = models.ForeignKey(ThirdLevelCategories, verbose_name=_('product category') ,null=True, on_delete=models.CASCADE)
    product_short_description = models.TextField(_('product short description'), null=True, blank=True)
    manufacturer = models.CharField(_('manufactered'), max_length=200, null=True, blank=True)
    for_sell_rent = models.CharField(verbose_name=_("For sell, rent or both"), max_length=40, choices=CHOICES, blank=True, null=True)
    model = models.CharField(_('model'), max_length=200, null=True, blank=True)
   
    class Meta:
        verbose_name = _('Product Displayed')
        verbose_name_plural = _('Products Displayed')
           
    def __str__(self):
        return self.product_name

   
class ProductPhotos(models.Model):
    #photo_name = models.CharField(max_length=200, null=False)
    photo = models.ImageField(upload_to ='upload/', verbose_name=_('photo'), null=True, blank=True)
    product = models.ForeignKey(ProductsDisplayed, verbose_name= _('product'), null=True,  on_delete=models.CASCADE)
    #default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Product Photo')
        verbose_name_plural = _('Products Photos')
    '''def __str__(self):
        return self.photo_name'''

#  ------------------ Around Specifications --------------------------- #

class CaseSealerSpecs(models.Model):
    TYPES = (
        ('BtmDr', 'Bottom Driven'),
        ('SdDr', 'Side Driven'),
        ('T&BtmDr', 'Top & Bottom Driven')
    )
    product = models.OneToOneField(ProductsDisplayed, verbose_name=_('product'), on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Case Sealer Type"), max_length=25, choices=TYPES, blank=True, null=True)
    min_box_size_cm = models.PositiveIntegerField(verbose_name=_("Minimum Box Size (cm)"), default=10, validators=[MinValueValidator(1), MaxValueValidator(20)])
    max_box_size_cm = models.PositiveIntegerField(verbose_name=_("Maximum Box Size (cm)"), default=20, validators=[MinValueValidator(1), MaxValueValidator(100)])
    boxes_per_min = models.PositiveIntegerField(verbose_name=_("Maximum boxes per min"), default=5, validators=[MinValueValidator(1), MaxValueValidator(100)])
    class Meta:
        verbose_name = _('Case Sealers Spec')
        verbose_name_plural = _('Case Sealers Specs')

    def __str__(self):
        return f"{self.product.id}. {self.product.product_name} specs"

class CasePackerSpecs(models.Model):
    TYPES = (
        ('top', 'Top Loader'),
        ('side', 'Side Loader'),
        ('P&PL', 'Pick and Place')
    )
    product = models.OneToOneField(ProductsDisplayed, verbose_name= _('product'),on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Case Packer Type"), max_length=25, choices=TYPES, blank=True, null=True)
    boxes_per_min = models.PositiveIntegerField(verbose_name=_("Maximum boxes per min"), default=5, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    class Meta:
        verbose_name = _('Case Packer spec')
        verbose_name_plural = _('Case Packer specs')
    
    def __str__(self):
        return f"{self.product.id}. {self.product.product_name} specs"
    

class DispersersSpecs(models.Model):
    TYPES = (
        ('batch', 'Batch'),
        ('continuous', 'Continuous')
    )
    product = models.OneToOneField(ProductsDisplayed, verbose_name=_('product'), on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Batch/Continuous"), max_length=25, choices=TYPES, blank=True, null=True)
    power = models.FloatField(verbose_name=_("Motor Power in kW"))
    application = models.CharField(verbose_name=_("Application"), max_length=80, blank=True, null=True)

    class Meta:
        verbose_name = _('Disperesers spec')
        verbose_name_plural = _('Dispereser specs')

    def __str__(self):
        return f"{self.product.id}. {self.product.product_name} specs"


class PalletizerSpecs(models.Model):
    TYPES = (
        ('layer', 'Layer'),
        ('gantry', 'Gantry'),
        ('robotic', 'Robotic'),
        ('other', 'Other')
    )
    product = models.OneToOneField(ProductsDisplayed, verbose_name=_('product'), on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Palletizer Type"), max_length=25, choices=TYPES, blank=True, null=True)
    throughput = models.FloatField(verbose_name=_("Throughput (pieces/min)"))
    application = models.CharField(verbose_name=_("Application"), max_length=80, blank=True, null=True)

    class Meta:
        verbose_name = _('Palletizer spec')
        verbose_name_plural = _('Palletizer specs')
    
    def __str__(self):
        return f"{self.product.id}. {self.product.product_name} specs"
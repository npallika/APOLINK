from django import forms
from django.forms import widgets, formset_factory , modelformset_factory, BaseFormSet
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import CheckboxInput
#from Accounts.models import PlatformUsers, Address, Country, Industry_Type
from Accounts.models import PlatformUsersAll, Country, Industry_Type
from .models import ProductsDisplayed, ProductPhotos, CaseSealerSpecs, CasePackerSpecs, DispersersSpecs, ThirdLevelCategories, PalletizerSpecs
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
#from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.utils.translation import gettext_lazy as _
from modeltranslation.utils import get_translation_fields




class DateInput(forms.DateInput):
    input_type = 'date'


class SellRentForm(forms.ModelForm):
    class Meta:
        model = ProductsDisplayed
        fields = ['manufactured_date' , 'product_name', 'product_category', 'product_short_description', 'manufacturer', 'for_sell_rent', 'model' ]
        #exclude = ['user', 'date_registered', 'date_updated',]
        widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }
        labels = {
            'manufactured_date': _('manufactured date'), 
            'product_name': _('product name'),
            'product_category': _('product category'),
            'product_short_description': _('product short description'),
            'manufacturer': _('manufacturer'),
            'for_sell_rent':_('For sell, rent or both'),
            'model': _('model'),
            }



class ProductPhotosForm(forms.ModelForm):
    photo=forms.ImageField(label=_('Upload image') , validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif']), validate_image_file_extension], error_messages={'invalid_image': 'Only .jpg, .jpeg, and .png files are allowed.'}) #changed from FileField
    class Meta:
        model = ProductPhotos
        fields = ['photo']
        widgets = { 'photo' : forms.FileInput(attrs={'class': 'photos-form'}) }
        
       
class ProductPhotosFormSet(forms.BaseModelFormSet):            
    def get_deletion_widget(self):
        return CheckboxInput(attrs={'class': 'deletion', 'type': 'checkbox', 'name': 'deletion', 'size': '1'})
    

PhotoFormSet = formset_factory(ProductPhotosForm, extra=3, max_num=3)

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = ProductsDisplayed
        fields = ['product_name', 'manufactured_date', 'product_category', 'manufacturer', 'model','for_sell_rent', 'product_short_description']
        labels = {
            'product_name': _('Product Name'),
            'manufactured_date': _('Manufactured date'),
            'product_category': _('Product Category'),
            'manufacturer': _('Manufacturer'),
            'model': _('Model'),
            'for_sell_rent': _('For sell, rent, or both'),
            'product_short_description': _('Product short description'),
            
        }
        #widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }

#  ------------------ Around Categories Specifications --------------------------- #

def TechSpecs(Model):
    #all_fields = ['type', 'min_box_size_cm', 'max_box_size_cm', 'boxes_per_min',]
    all_fields = []
    #YOU DELETED THE FIELDS : MAYBE IS USELESS THIS PART :
    for field in Model._meta.get_fields():
        if field.name != 'product' and field.name != 'id' and ('_en' not in field.name) and ('_el' not in field.name):
            all_fields.append(field.name)
            
   
    print(all_fields)
    class TechSpecsForm(forms.ModelForm):
        class Meta:
            model = Model
            #fields = all_fields
            exclude = ['product']
          
            
    
    return TechSpecsForm

'''class CaseSealersTechSpecsForm(forms.ModelForm):
    class Meta:
        model = CaseSealerSpecs
        exclude = ['product']
        

class CasePackerTechSpecsForm(forms.ModelForm):
    class Meta:
        model = CasePackerSpecs
        exclude = ['product']
        #fields = '__all__'


class DispersersTechSpecsForm(forms.ModelForm):
    class Meta:
        model = DispersersSpecs
        exclude = ['product']
        

class PalletizersTechSpecsForm(forms.ModelForm):
    class Meta:
        model = PalletizerSpecs
        exclude = ['product']
        '''
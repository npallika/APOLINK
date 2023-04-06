from django import forms
from django.forms import widgets, formset_factory , modelformset_factory, BaseFormSet
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import CheckboxInput
from Accounts.models import PlatformUsers, Address, Country, Industry_Type
from .models import ProductsDisplayed, ProductPhotos, CaseSealerSpecs, CasePackerSpecs, DispersersSpecs, ThirdLevelCategories
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
#from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, validate_image_file_extension






class DateInput(forms.DateInput):
    input_type = 'date'


class SellRentForm(forms.ModelForm):
    class Meta:
        model = ProductsDisplayed
        exclude = ['user', 'date_registered', 'date_updated']
        widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }



class ProductPhotosForm(forms.ModelForm):
    photo=forms.ImageField(label='Upload image' , validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif']), validate_image_file_extension], error_messages={'invalid_image': 'Only .jpg, .jpeg, and .png files are allowed.'}) #changed from FileField
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
        widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }

#  ------------------ Around Categories Specifications --------------------------- #

class CaseSealersTechSpecsForm(forms.ModelForm):
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



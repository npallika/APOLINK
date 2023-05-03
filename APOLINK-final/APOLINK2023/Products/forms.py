from django import forms
from django.forms import widgets, formset_factory , modelformset_factory
from django.forms.widgets import CheckboxInput
from .models import ProductsDisplayed, ProductPhotos, Contact
from datetime import datetime
#from captcha.fields import CaptchaField
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.utils.translation import gettext_lazy as _


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
    #photo field is validated with a django built-in validator, passing a django function to check for valid extensions
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
            'for_sell_rent': _('For sell, rent or both'),
            'product_short_description': _('Product short description'),
            
        }
        #widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }


class ContactForm(forms.ModelForm):
    #cc_myself = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control', 'required': 'false'}))
    class Meta:
        model = Contact
        fields = ['subject', 'message', 'reason']
        labels={
            'subject': _('Subject'),
            'message': _('Message'),
            'reason': _('Reason'),
        }
    #possible implementation to move the complexity from views to forms.py: is applyable wherever you need to put a condition on diplayed fields
    '''
    def __init__(self, *args, **kwargs):
        print(kwargs)
        user = kwargs.pop('user')
        print(kwargs)
        super().__init__(*args, **kwargs)
        if not user.is_authenticated:
            self.fields.pop('email')
            self.fields.pop('username')
            self.fields.pop('lastName')
    '''




#  ------------------ Around Categories Specifications --------------------------- #

def TechSpecs(Model):
    all_fields = []
    #you have to use this for if you have some problems with sufixes of translated fields
    '''
    for field in Model._meta.get_fields():
        if field.name != 'product' and field.name != 'id' and ('_en' not in field.name) and ('_el' not in field.name):
            all_fields.append(field.name)
    '''
    class TechSpecsForm(forms.ModelForm):
        class Meta:
            model = Model
            #fields = all_fields
            exclude = ['product']
    return TechSpecsForm


#OLD IMPLEMENTATION: separated forms for every product specs
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
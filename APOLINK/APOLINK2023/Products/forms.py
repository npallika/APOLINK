from django import forms
from django.forms import widgets, formset_factory 
from django.contrib.admin.widgets import AdminDateWidget
from Accounts.models import PlatformUsers, Address, Country, Industry_Type
from .models import ProductsDisplayed, ProductPhotos, CaseSealerSpecs, CasePackerSpecs, DispersersSpecs, ThirdLevelCategories
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
#from captcha.fields import CaptchaField
from django.contrib.auth.models import User





class DateInput(forms.DateInput):
    input_type = 'date'


class SellRentForm(forms.ModelForm):
    
    
    class Meta:
        model = ProductsDisplayed
        #fields = '__all__'
        exclude = ['user', 'date_registered', 'date_updated']
        widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_category'].queryset = ThirdLevelCategories.objects.none()

    def clean_category(self):
        category_name = self.cleaned_data.get('category_name')
        if not category_name:
            raise forms.ValidationError('Please enter a category name.')

        categories = ThirdLevelCategories.objects.filter(name__icontains=category_name)
        if not categories:
            raise forms.ValidationError('No matching categories found.')

        if len(categories) > 1:
            category_choices = [(c.id, c.name) for c in categories]
            self.fields['category'].widget = forms.RadioSelect(choices=category_choices)

            raise forms.ValidationError('Multiple matching categories found. Please choose one from the list.')

        product_category = categories.first()
        return product_category
'''
   
class ProductPhotosForm(forms.ModelForm):
    photo=forms.FileField(label='Upload image')
    class Meta:
        model = ProductPhotos
        fields = ['photo']
       
PhotoFormSet = formset_factory(ProductPhotosForm, extra=3, max_num=3)


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = ProductsDisplayed
        fields = ['product_name', 'manufactured_date', 'product_category', 'manufacturer', 'model','for_sell_rent', 'product_short_description']
        widgets = { 'manufactured_date' : DateInput(attrs={'type':'date', 'max': datetime.now().time()}) }

#  ------------------ Around Categories Specifications --------------------------- #

class CaseSealersTechSpecsForm(forms.ModelForm):
    #product = forms.IntegerField(widget=forms.HiddenInput(), initial=ProductsDisplayed.objects.all().first().id)
    
    class Meta:
        model = CaseSealerSpecs
        exclude = ['product']
        

class CasePackerTechSpecsForm(forms.ModelForm):
    #product = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = CasePackerSpecs
        exclude = ['product']
        #fields = '__all__'


class DispersersTechSpecsForm(forms.ModelForm):
    #product = forms.IntegerField(widget=forms.HiddenInput(), initial=ProductsDisplayed.objects.all().first().id)

    class Meta:
        model = DispersersSpecs
        exclude = ['product']



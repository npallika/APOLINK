from django.shortcuts import render, redirect, get_object_or_404
from django.forms.formsets import formset_factory 
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django.http import HttpResponseRedirect
from .models import ProductsDisplayed, ProductPhotos, ThirdLevelCategories,DispersersSpecs,CaseSealerSpecs, CasePackerSpecs
from .forms import UserCreationForm, SellRentForm, UpdateProductForm, PhotoFormSet, CaseSealersTechSpecsForm, CasePackerTechSpecsForm, DispersersTechSpecsForm
from django.db import models
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Core.models import FirstLevelCategories, SecondLevelCategories
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
# Create your views here.

def CategoriesProductsList(request, slug):
    category = ThirdLevelCategories.objects.get(slug=slug)
    products_per_category = ProductsDisplayed.objects.filter(product_category=category)
    product_photos = {}
    for product in products_per_category:
        product_photos[product] = ProductPhotos.objects.filter(product=product).first()
        photo = ProductPhotos.objects.filter(product=product).first()
    
    return render(request, 'Products/category_products_list.html', 
                {'product_photos':product_photos,
                'products_category':category})

'''
class CategoriesProductsListView(DetailView):
    context_object_name = 'products_category'
    model = ThirdLevelCategories
    template_name = 'Products/category_products_list.html'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['Products_in_category'] = ProductsDisplayed.objects.all()
       
        return context

'''

class ProductDetails(DetailView):
    context_object_name = 'product_detail'
    model = ProductsDisplayed
    template_name = 'Products/product_details.html'        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Photos'] = ProductPhotos.objects.all()
        return context


models_dict = {
    'Case Sealers':CaseSealerSpecs,
    'Case Packers':CasePackerSpecs,
    'Dispersers-Mixers':DispersersSpecs,
}



def ProductSelected(request, pk):
    product_selected = get_object_or_404(ProductsDisplayed, id=pk)
    photos = ProductPhotos.objects.filter(product=product_selected)
    category_name = product_selected.product_category.name
    model_specs = models_dict[category_name]
    try:
        tech_specs = model_specs.objects.get(product=product_selected)
        print(f"tech specs {vars(tech_specs)}")
        attributes = {k:v for k,v in vars(tech_specs).items() if k not in ['product','_state','id','product_id']}
        print(f"The Tech specs are {attributes}")       
        context = {'product_selected':product_selected, 'Photos':photos,
            'attributes': [{
            'verbose_name': tech_specs._meta.get_field(attr_name).verbose_name,
            'value': tech_specs.get_type_display() if isinstance(tech_specs._meta.get_field(attr_name), models.Field) and tech_specs._meta.get_field(attr_name).choices else attr_value,
            } for attr_name, attr_value in attributes.items()]}
    except:
        attributes = None
        context = {'product_selected':product_selected, 'Photos':photos,
            'attributes':attributes }
    
    return render(request, 'Products/product_details.html', context)

def search_product(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = ProductsDisplayed.objects.filter(product_name__contains=searched)
        return render(request, 'Products/search_products.html', {'searched':searched, 'products':products})
    else:        
        return render(request, 'Products/search_products.html', {})


@login_required
def sell_rent(request):
    sellRentForm = SellRentForm()
    formset = PhotoFormSet(prefix="photos")
       
    if request.method == 'POST':
        sellRentForm = SellRentForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES, prefix="photos")
        
        if sellRentForm.is_valid() and formset.is_valid(): 
            publish=sellRentForm.save(commit=False)
            publish.user= request.user #save a new Product associated with the user logged - in (foreign key)
            publish.save()
            
            print ("The Id of the product is %s" %(publish.id))
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.product = publish
                    photo.save()
            messages.success(request, 'Photos uploaded succesfully')
            return redirect ('Products:technical_specs', pk=publish.id)
        else:
          #formset is not valid : is read the validator passed to the field
            
          messages.error(request, 'There was an error uploading your photos. Please ensure that the uploaded files are images.')
            
    else:     
        sellRentForm = SellRentForm()

    return render(request, 'Products/sellRent_form.html', {'sellRentForm': sellRentForm, 'formset': formset  })


models_form_dict = {
    'Case Sealers':CaseSealersTechSpecsForm,
    'Case Packers':CasePackerTechSpecsForm,
    'Dispersers-Mixers':DispersersTechSpecsForm
}



@login_required
def ProductsSpecsCreate(request, pk):
    try:
        product = ProductsDisplayed.objects.get(id=pk)
        #print(f"The product is: {product}")
    except ProductsDisplayed.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect('products_category')

    #product = get_object_or_404(ProductsDisplayed, pk=pk)
    
    category = product.product_category
    category_name = category.name
    #print(f"The category name is: {category_name}")
    #ProductSpecsForm = models_form_dict[category_name]()
    
    if request.method == 'POST':
        #print("Now, I post!")
        ProductSpecsForm = models_form_dict[category_name](request.POST)
        #ProductSpecsForm.product = product
        #print(f"Contents of the form: {ProductSpecsForm}")
        if ProductSpecsForm.is_valid():
            publish=ProductSpecsForm.save(commit=False)
            #print (f"The publish is {publish}")
            publish.product = product   
            publish.save()
            #print (publish.product)
            
            return redirect ('Products:product_details', pk)

    else:
        ProductSpecsForm = models_form_dict[category_name]()
            
    return render(request, 'Products/techSpecsForm.html', {'ProductsTechSpecs': ProductSpecsForm})


@login_required
def show_my_products(request):
    user = request.user
    my_products=[]
    try:
        my_products = ProductsDisplayed.objects.filter(user=user)
        product_photos = {}
        for product in my_products:
            print(f"Product.id type: {type(product.id)}")
            product_photos[product] = ProductPhotos.objects.filter(product=product).first()
            photo = ProductPhotos.objects.filter(product=product).first()
    #my_photos = ProductPhotos.objects.filter(product__in = my_products)
    #for photo in my_photos:
    #    print(photo)
        print(f"Product photos:{product_photos}")
        return render(request, 'Products/show_my_products.html', {'product_photos':product_photos, 'image':photo })
    except:
        return render(request, 'Products/show_my_products.html', {'product_photos':product_photos})

@login_required
def delete_product(request, product_id):
    product = ProductsDisplayed.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('Products:show_my_products')
    return render(request, 'Products/delete_product.html', {'product': product})


@login_required
def update_product(request, product_id):
    product = ProductsDisplayed.objects.get(id=product_id)
    initial_data = [{'id': photo.id, 'photo':photo.photo} for photo in product.productphotos_set.all()]
    #PhotoFormSet = formset_factory(ProductPhotosForm, extra=0)
    
    if request.method == 'POST':
        #print(f"The request.POST is {request.POST}")
        #print(f"The request.FILES is {request.FILES}")
        form = UpdateProductForm(request.POST, instance=product)
        formset = PhotoFormSet(request.POST or None, request.FILES or None, prefix='photos')
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset:
                if form.cleaned_data.get('id'):
                    photo = ProductPhotos.objects.get(id=form.cleaned_data.get('id'))
                    photo.photo = form.cleaned_data.get('form')
                    photo.save()
                else:
                    photo = form.save(commit=False)
                    photo.product = product
                    photo.save()
                    
                    
            #return redirect ('Products:technical_specs', pk=publish.id)
            return redirect('Products:show_my_products')
    else:
        form = UpdateProductForm(instance=product)
        formset = PhotoFormSet(prefix='photos')
        for photo in product.productphotos_set.all():
            form = formset.empty_form.copy()
            form['id'].field.initial = photo.id
            form['photo'].field.initial = photo.photo
            formset.append_form(form)
        #print(f"The formset is {formset}")
    return render(request, 'Products/update_product.html',  {'form': form, 'formset': formset})
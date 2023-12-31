from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from .models import ProductsDisplayed, ProductPhotos, ThirdLevelCategories,DispersersSpecs,CaseSealerSpecs, CasePackerSpecs, PalletizerSpecs
from .forms import SellRentForm, UpdateProductForm, ProductPhotosForm, PhotoFormSet,ProductPhotosFormSet, TechSpecs, ContactForm #LoginForm
from django.db import models
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView)
from django.contrib import messages
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.safestring import mark_safe

# Create your views here.

#function to retrive the right Specs Model in order to achive the right Form
def get_models():
    models_dict = {
    force_str(_('Case Sealers')):CaseSealerSpecs,
    force_str(_('Case Packers')):CasePackerSpecs,
    force_str(_('Dispersers-Mixers')):DispersersSpecs,
    force_str(_('Palletizers')): PalletizerSpecs,
    }
    return models_dict


#function to send contact email to the seller from the session user
def sendContactEmail(request, **kwargs):
    subject = kwargs.get('subject')
    user = kwargs.get('user')
    to_email = kwargs.get('to_email')
    seller = kwargs.get('seller')
    message_email = kwargs.get('message')
    reason = kwargs.get('reason')
    product = kwargs.get('product')
    #send a message contained in a template, pass context
    message = render_to_string(
        'Products/contact_email.html',
        {'user': user,
         'seller': seller,
         'reason': reason,
         'message_email': message_email,
         'product': product,
         'domain': get_current_site(request).domain,
        #'uid': urlsafe_base64_encode(force_bytes(seller.pk)), #necessary for hiding user.pk in URL
         'protocol': 'https' if request.is_secure() else 'http'
         }
    )
    email = EmailMessage(subject, 
                         message, 
                         to=[to_email]) #seller email
    email.content_subtype='html'
    if email.send(): #return 1 if the email is sent correctly
        msg = _('Dear <b>{username}</b>, you correctly contacted the seller at the email: <b>{to_email}</b>')
        msg = format_html(msg, username =user.username, to_email=to_email)  # insert the translated variables into the message and mark it as safe
        messages.success(request, msg)  # show the translated message
    else :
        messages.error(request, mark_safe(_(f'Problem sending email to {to_email}', 'check if you typed it correctly')))
    pass
    

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


def ProductSelected(request, pk):
    models_dict = get_models()
    product_selected = get_object_or_404(ProductsDisplayed, id=pk)
    photos = ProductPhotos.objects.filter(product=product_selected)
    category_name = product_selected.product_category.name
    model_specs = models_dict.get(category_name, None)
    seller = product_selected.user
    user = request.user
    productContacts = product_selected.contact_set.all()
    n_contacts = productContacts.count()
    try:
        tech_specs = model_specs.objects.get(product=product_selected)
        attributes = {k:v for k,v in vars(tech_specs).items() if k not in ['product','_state','id','product_id']}     
        context = {
            'product_selected':product_selected,
            'seller': seller,
            'user': user,
            'n_contacts':n_contacts,
            'Photos':photos,
            'attributes': [{
            'verbose_name': tech_specs._meta.get_field(attr_name).verbose_name,
            'value': tech_specs.get_type_display() if isinstance(tech_specs._meta.get_field(attr_name), models.Field) and tech_specs._meta.get_field(attr_name).choices else attr_value,
            } for attr_name, attr_value in attributes.items()],
            }
    except:
        attributes = None
        context = {
            'product_selected':product_selected, 
            'Photos':photos,
            'attributes':attributes }
    #----if you are logged-in:
    if user.is_authenticated:
        if request.method == 'POST':
            contactForm = ContactForm(request.POST)
            if contactForm.is_valid():
                contact = contactForm.save(commit=False) #save the product before commit
                contact.product= product_selected
                contact.save()
                sendContactEmail(request, user= user, seller =seller, to_email = seller.email, 
                                subject= contactForm.cleaned_data.get('subject'), 
                                message= contactForm.cleaned_data.get('message'), 
                                reason = contactForm.cleaned_data.get('reason'), 
                                product = product_selected)
                #Update context with contact form 
                return redirect('Products:product_details', product_selected.pk)     
            else:
                messages.error(request, _('ERROR in form validation'))   
            
        else: 
            contactForm= ContactForm()
            context.update({'form_contact': contactForm})
    #----if you are not logged in: pop-up login
    else:
        if request.method == 'POST':
            loginForm = AuthenticationForm(request, data=request.POST)
            if loginForm.is_valid():
                username = loginForm.cleaned_data.get('username')
                password = loginForm.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user and user.is_active:
                    login(request, user)
                    messages.success(request, _('You have successfully logged in')) 
                    return redirect('Products:product_details', product_selected.pk)
                else:
                    messages.warning(request, _('Your account is not active.'))
            else:
                messages.error(request, "ERROR: Invalid username or password")      
        else :
            loginForm = AuthenticationForm()
            context.update({'form_login': loginForm}) 
    return render(request, 'Products/product_details.html', context)
    #CODE MORE EFFICIENT, BUT MORE COMPLICATED
    '''
    if request.method == 'POST':
        if not user.is_authenticated:
            loginForm = AuthenticationForm(request, data=request.POST)
            if loginForm.is_valid():
                username = loginForm.cleaned_data.get('username')
                password = loginForm.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user and user.is_active:
                    login(request, user)
                    messages.success(request, _('You have successfully logged in'))
                    
                    contactForm = ContactForm()
                    context.update({'form_contact': contactForm})
                    return redirect('Products:product_details', product_selected.pk)
                else:
                    messages.warning(request, 'Your account is not active.')
        else:
            contactForm= ContactForm(request.POST)
            if contactForm.is_valid():
                contact = contactForm.save(commit=False) #save the product before commit
                contact.product= product_selected
                contact.save()
                sendContactEmail(request, user= user, seller =seller, to_email = seller.email, 
                                subject= contactForm.cleaned_data.get('subject'), 
                                message= contactForm.cleaned_data.get('message'), 
                                reason = contactForm.cleaned_data.get('reason'), 
                                product = product_selected)         
    else:
        if not user.is_authenticated:
            loginForm = AuthenticationForm()    
            context.update({'form_login': loginForm})
        else:
            contactForm = ContactForm()
            context.update({'form_contact': contactForm})
    return render(request, 'Products/product_details.html', context)
    '''


@login_required
def MyProductInfo(request, pk):
    models_dict = get_models()
    product_selected = get_object_or_404(ProductsDisplayed, id=pk)
    photos = ProductPhotos.objects.filter(product=product_selected)
    category_name = product_selected.product_category.name
    model_specs = models_dict.get(category_name, None)
    try:
        tech_specs = model_specs.objects.get(product=product_selected)
        print(f"tech specs {vars(tech_specs)}")
        attributes = {k:v for k,v in vars(tech_specs).items() if k not in ['product','_state','id','product_id']}      
        context = {
            'product_selected':product_selected, 
            'Photos':photos,
            'attributes': [{
            'verbose_name': tech_specs._meta.get_field(attr_name).verbose_name,
            'value': tech_specs.get_type_display() if isinstance(tech_specs._meta.get_field(attr_name), models.Field) and tech_specs._meta.get_field(attr_name).choices else attr_value,
            } for attr_name, attr_value in attributes.items()],
            }
    except:
        attributes = None
        context = {'product_selected':product_selected, 'Photos':photos,
            'attributes':attributes }
    return render(request, 'Products/my_product_info.html', context)


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
        formset = PhotoFormSet(request.POST, request.FILES, prefix="photos") #mandatory passing request.FILES
        if sellRentForm.is_valid() and formset.is_valid(): 
            #when you are saving "for_sell_rent" field in greek , you can show it just if you are in greek
            publish=sellRentForm.save(commit=False)
            publish.user= request.user #save a new Product associated with the user logged - in (foreign key)
            publish.save()    
            #print ("The Id of the product is %s" %(publish.id))
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.product = publish
                    photo.save()
            messages.success(request, _('Product uploaded succesfully'))
            return redirect ('Products:technical_specs', pk=publish.id)
        else:
          #formset is not valid : is read the validator passed to the field
          messages.error(request, _('There was an error uploading your photos. Please ensure that the uploaded files are images.'))    
    else:     
        sellRentForm = SellRentForm()
    return render(request, 'Products/sellRent_form.html', {'sellRentForm': sellRentForm, 'formset': formset  })




@login_required
def ProductsSpecsCreate(request, pk):
    models_dict = get_models()
    try:
        product = ProductsDisplayed.objects.get(id=pk)
    except ProductsDisplayed.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect('Products:products_category')
    category_name = product.product_category.name
    model_specs = models_dict.get(category_name, None)
    category = product.product_category #third level cat object
    category_name = category.name
    #if you find a specs related to the product yet -> redirect to an create page for updating
    try:
        specsCategory = model_specs.objects.get(product=product)
    except:
        pass
    else:
        if request.method == 'POST':
            ProductSpecsForm = TechSpecs(models_dict.get(category_name, None))(request.POST, instance=specsCategory)
            if ProductSpecsForm.is_valid():
                publish=ProductSpecsForm.save(commit=False)
                publish.product = product   
                publish.save()
            return redirect ('Products:myProductInfo', pk)
        else:
           ProductSpecsForm = TechSpecs(models_dict.get(category_name,None))(instance=specsCategory) 
           return render(request, 'Products/techSpecsForm.html', {'ProductsTechSpecs': ProductSpecsForm})
    
    if request.method == 'POST':
        ProductSpecsForm = TechSpecs(models_dict.get(category_name, None))(request.POST)
        if ProductSpecsForm.is_valid():
            publish=ProductSpecsForm.save(commit=False)
            publish.product = product   
            publish.save()
            return redirect ('Products:myProductInfo', pk) #product_details of my products
    else:
        ProductSpecsForm = TechSpecs(models_dict.get(category_name, None))() #take the right form from dictionary based on thirdlevelcategory
    return render(request, 'Products/techSpecsForm.html', {'ProductsTechSpecs': ProductSpecsForm})


@login_required
def ProductsSpecsUpdate(request, pk):
    models_dict = get_models()
    try:
        product = ProductsDisplayed.objects.get(id=pk)
    except ProductsDisplayed.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect('products_category')
    category = product.product_category #third level cat object
    category_name = category.name
    specsModel = models_dict.get(category_name, None) #model of the specs of that product
    try:
        specsCategory = specsModel.objects.get(product=product) #take one-to-one specs of the product
    except specsModel.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect('Products:technical_specs', pk)
   
    if request.method == 'POST':
        #ProductSpecsForm = models_form_dict[category_name](request.POST, instance=specsCategory)
        ProductSpecsForm = TechSpecs(models_dict[category_name])(request.POST, instance=specsCategory)  
        if ProductSpecsForm.is_valid():
            publish=ProductSpecsForm.save(commit=False)
            publish.product = product   
            publish.save()
            return redirect ('Products:myProductInfo', pk) #Products:product_details
    else:
        ProductSpecsForm = TechSpecs(models_dict.get(category_name,None))(instance=specsCategory)#take the right form from dictionary based on thirdlevelcategory     
    return render(request, 'Products/techSpecsForm.html', {'ProductsTechSpecs': ProductSpecsForm})


@login_required
def show_my_products(request):
    user = request.user
    my_products=[]
    try:
        my_products = ProductsDisplayed.objects.filter(user=user)
        product_photos = {}
        for product in my_products:
            product_photos[product] = ProductPhotos.objects.filter(product=product).first()
            photo = ProductPhotos.objects.filter(product=product).first()
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
    product = get_object_or_404(ProductsDisplayed, id=product_id) #take the product clicked
    productPhotos = product.productphotos_set.all() #take all the photos related to that product (product_id)
    #model formset is a way to create directly from a Model and Form a formset with some features addable
    UpdateFormset = modelformset_factory(ProductPhotos, form=ProductPhotosForm ,formset= ProductPhotosFormSet ,extra=3, max_num=3, validate_max=True, can_delete=True, can_delete_extra=True)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, instance=product)
        formset = UpdateFormset(request.POST or None, request.FILES or None, queryset=productPhotos, prefix='photos')
        if form.is_valid() and formset.is_valid():
            product = form.save() #save the updated product
            product.save()
            #UPDATE : i need manually to set every product per photos, because so far i updated just the photos
            #if you click on delete button , delete the photo related to that product
            for form in formset:
                if form.cleaned_data: #if i have any photos in my forms
                    print(f"CLEANED DATA : {form.cleaned_data}")
                    photo = form.save(commit=False) #take the instance from model
                    print(photo)
                    photo.product = product
                    if form.cleaned_data["DELETE"]==True:
                        photo.delete()
                    else:
                        photo.save()
                    
            formset.save() #returns istances saved in database, just if are filled in the form                        
            return redirect('Products:technical_specs_update', product_id)
        else:
            print(f"ERROR IN FORMSET : {formset.non_form_errors()}")
        
    else:
        # UPDATING FORMS
        form = UpdateProductForm(instance=product) #take precompiled form of that Product
        print(f"OBJECT : {product} : {productPhotos}")
        formset = UpdateFormset(queryset= productPhotos, prefix='photos')
    return render(request, 'Products/update_product.html',  {'form': form, 'formset': formset, 'product': product})



#ANOTHER POSSIBLE IMPLEMENTATION: manage photos deleation
def delete_image(request, pk):
    try:
        photo = photo.objects.get(id=pk)
    except photo.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('Products:update_product', pk=photo.product.id)

    photo.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('products:update_product', pk=photo.product.id)
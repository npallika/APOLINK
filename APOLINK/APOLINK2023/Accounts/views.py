from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from django import forms
from django.forms.formsets import formset_factory 
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib import messages
from django.views import generic
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import UserCreationForm, PlatformUsersForm, AddressForm
from Core import models
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

# pip install django-braces


# Create your views here.

'''class SignUp ( CreateView ) :    
    form_class = forms.UserCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy( 'Core:categories_list' )   
'''
# class SignUpDetail (CreateView):
     
def Signup(request):
    if request.method == "POST":
        userForm = UserCreationForm(request.POST)
        print(f"Ther UserCreatonForm is {userForm}")
        userInfoForm = PlatformUsersForm(request.POST)
        addressForm = AddressForm(request.POST)
        if userForm.is_valid() and addressForm.is_valid() and userInfoForm.is_valid() :
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            address = addressForm.save()
            user_info = userInfoForm.save(commit=False)
            user_info.user=user
            user_info.main_address = address            

            user_info.save()      
            return HttpResponseRedirect(reverse('Accounts:login'))  
    else:
        userForm = UserCreationForm()
        userInfoForm = PlatformUsersForm()
        addressForm = AddressForm()
        print(f"Ther UserCreatonForm is {userForm}")
    return render(request, 'accounts/signup.html', {'userForm': userForm, 'userInfoForm': userInfoForm, 'addressForm': addressForm})


'''def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('Core:categories_list'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'accounts/login.html', {})
'''
@login_required
def user_logout(request):
    # Log out the user.
    messages.info(request, "You have successfully logged out.") 
    logout(request)
    # Return to homepage.
    return redirect("Core:categories_list")
    '''HttpResponseRedirect(reverse('Accounts:login'))'''    




'''class CreateSellRent(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    template_name = 'Accounts/sellRent_form.html'
    model = models.ProductsDisplayed
    form_class = CrSR
    #fields = ['date_registered', 'manufactured_date', 'product_name','product_category', 'product_short_description']
    
    success_url = reverse_lazy('Core:categories_list')
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
'''

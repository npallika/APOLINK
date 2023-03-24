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


# pip install django-braces

def Signup(request):
    if request.method == "POST":
        userForm = UserCreationForm(request.POST)
        userInfoForm = PlatformUsersForm(request.POST)
        addressForm = AddressForm(request.POST)
        if userForm.is_valid() and addressForm.is_valid() and userInfoForm.is_valid() :
            user = userForm.save()
                
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
        
    return render(request, 'accounts/signup.html', {'userForm': userForm, 'userInfoForm': userInfoForm, 'addressForm': addressForm})


@login_required
def user_logout(request):
    # Log out the user.
    messages.info(request, "You have successfully logged out.") 
    logout(request)
    # Return to homepage.
    return redirect("Core:categories_list")
    








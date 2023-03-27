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
from django.core.mail import EmailMessage, get_connection, send_mail
from .tokens import account_activation_token

# pip install django-braces
def activateEmail(request, user, to_email):
    messages.success(request, f'Dear<b>{user}</b>, please go to email <b>{to_email}</b> inbox and click on received activation link to ocnfirm and complete the registration.<b> Note: </b>. Check your spam folder.')
    
def Signup(request):
    if request.method == "POST":
        userForm = UserCreationForm(request.POST)
        print(f"Ther UserCreatonForm is {userForm}")
        userInfoForm = PlatformUsersForm(request.POST)
        addressForm = AddressForm(request.POST)
        if userForm.is_valid() and addressForm.is_valid() and userInfoForm.is_valid() :
            user = userForm.save(commit=False) #don't save immediatley in DB (first email verification)
            user.is_active = False #not yet activated, email verification first
            user.set_password(user.password)
            user.save()
            
            address = addressForm.save(commit=False)
            user_info = userInfoForm.save(commit=False)
            user_info.user=user
            user_info.main_address = address            
            user_info.save()     
            activateEmail(request, user, userForm.cleaned_data.get('email')) #if the user SIGN-UP, compare this message: go to email and confirm 
            return HttpResponseRedirect(reverse('Accounts:login'))  
    else:
        userForm = UserCreationForm() #User auth connection
        userInfoForm = PlatformUsersForm() #user auth + added information
        addressForm = AddressForm() #added information of address of User
        print(f"Ther UserCreatonForm is {userForm}")
    return render(request, 'accounts/signup.html', {'userForm': userForm, 'userInfoForm': userInfoForm, 'addressForm': addressForm})



@login_required
def user_logout(request):
    # Log out the user.
    messages.info(request, "You have successfully logged out.") 
    logout(request)
    # Return to homepage.
    return redirect("Core:categories_list")
    








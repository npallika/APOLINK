from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from django import forms
from django.forms.formsets import formset_factory 
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib import messages
from django.views import generic
from django.contrib.auth import authenticate,login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import UserCreationForm, PlatformUsersForm, AddressForm
from Core import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, get_connection, send_mail
from .tokens import account_activation_token

#EMAIL VERIFICATION
def Activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) #take the PK of the user by decoding URL
        user = User.objects.get(pk=uid)
    except:
        user=None
    #if we found a current user saved (not actived yet) + check the token
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save() #now user, already saved before, is saved again, but ACTIVE!
        messages.success(request, "Thank you for your email confirmation. Now you can LOGIN in your account")
        return HttpResponseRedirect(reverse('Accounts:login'))
    else:
        messages.error(request, "Activation link is invalid!")
    return HttpResponseRedirect(reverse('Core:categories_list'))


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account'
    #send a message contained in a template, pass context
    message = render_to_string(
        'Accounts/template_activate_account.html',
        {'user': user.username,
         'domain': get_current_site(request).domain,
         'uid': urlsafe_base64_encode(force_bytes(user.pk)), #necessary for hiding user.pk in URL
         'token': account_activation_token.make_token(user),
         'protocol': 'https' if request.is_secure() else 'http'
         }
    )
    email = EmailMessage(mail_subject, 
                         message, 
                         to=[to_email]) #user email
    email.content_subtype='html'
    if email.send(): #return 1 if the email is sent correctly
        messages.success(request, f'Dear <b>{user}</b>, please go to email <b>{to_email}</b> inbox and click on received activation link to confirm and complete the registration.<b> Note: </b>. Check your spam folder.')
    else :
        messages.error(request, f'Problem sending email to {to_email}', 'check if you typed it correctly')

    
# pip install django-braces
def Signup(request):
    if request.method == "POST":
        userForm = UserCreationForm(request.POST)
        print(f"Ther UserCreatonForm is {userForm}")
        userInfoForm = PlatformUsersForm(request.POST)
        addressForm = AddressForm(request.POST)
        if userForm.is_valid() and addressForm.is_valid() and userInfoForm.is_valid() :
            user = userForm.save(commit=False) #don't save immediatley in DB , first put active = False
            user.is_active = False #not yet activated, email verification first: activation through ACTIVATE VIEW
            user.set_password(user.password)
            user.save() #save as unactive before email verification
            
            #Address and user_info must be saved, in any case if i delete user, delete everything else
            address = addressForm.save()
            user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
            user_info.user=user
            user_info.main_address = address #note : if you delete user/platformUser -> not delete address created          
            user_info.save() 
            
            #activation email is sent after the user complete the form
            activateEmail(request, user, userForm.cleaned_data.get('email')) #if the user SIGN-UP, compare this message: go to email and confirm + sent email
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
    

class CustomLoginView(LoginView):
    #1) first is called with a GET : after clicking on email link
    #2) second is called with POST: user complete login form and is called again
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        #print(vars(user))
        if user is not None and user.is_active:
            # Access user's pk
            pk = user.pk
            # Perform login operation as usual
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Your account is not active.')
            #redirect('Accounts:login')
            return self.form_invalid(form)
    
    def post(self, request, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print((user))
        return super().post(request, **kwargs)

   
    
    






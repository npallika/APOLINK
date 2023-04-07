from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
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
from .forms import UserCreationForm, PlatformUsersFormAll
#from .forms import UserCreationForm, PlatformUsersForm, AddressForm, PlatformUsersForm
from .models import PlatformUsersAll
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
        print(f"USER FOUND {user} WITH PK = {uid} AND PASS = {user.password}")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
        print("User NOT FOUND")
    #if we found a current user saved (not actived yet) + check the token
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save() #now user, already saved before, is saved again, but ACTIVE!
        print(f"USER {vars(user)} HAS ACTIVE = {user.is_active}")
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
        userInfoForm = PlatformUsersFormAll(request.POST)
        #addressForm = AddressForm(request.POST)
        #and addressForm.is_valid()
        if userForm.is_valid()  and userInfoForm.is_valid() :
            user = userForm.save(commit=False) #don't save immediatley in DB , first put active = False
            #not yet activated, email verification first (activation) and don't set password!
            user.is_active = False 
            user.save() #save as unactive before email verification
            
            #Address and user_info must be saved, in any case if i delete user, delete everything else
            #address = addressForm.save()
            user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
            user_info.user=user
            #user_info.main_address = address #note : if you delete user/platformUser -> not delete address created          
            user_info.save() 
            
            #activation email is sent after the user complete the form
            activateEmail(request, user, userForm.cleaned_data.get('email')) #if the user SIGN-UP, compare this message: go to email and confirm + sent email
            return HttpResponseRedirect(reverse('Accounts:login'))  
    else:
        userForm = UserCreationForm() #User auth connection
        userInfoForm = PlatformUsersFormAll() #user auth + added information
        #addressForm = AddressForm() #added information of address of User
        #'addressForm': addressForm
    return render(request, 'accounts/signup.html', {'userForm': userForm, 'userInfoForm': userInfoForm})



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
            messages.success(self.request, 'You have successfully logged in')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Your account is not active.')
            #redirect('Accounts:login')
            return self.form_invalid(form)



@login_required
def AccountInfo(request, user_id):
    context={}
    try:
        user = User.objects.get(pk=user_id)
        userInfo = PlatformUsersAll.objects.get(user=user)
    except User.DoesNotExist and PlatformUsersAll.DoesNotExist:
        return HttpResponseRedirect(reverse('Accounts:signup'))
    
    context["id"] = user.id
    context["username"] = user.username
    context["password"] = user.password
    context["email"] = user.email
    context["company_name"] = userInfo.company_name
    context["industry"] = userInfo.industry
    context["address"] = userInfo.street_address

    # Define template variables
    is_self = True
    is_friend = False
    user = request.user
    if user.is_authenticated and user != userInfo.user:
        is_self = False
    elif not user.is_authenticated:
        is_self = False
        
    # Set the template variables to the values
    context['is_self'] = is_self
    context['is_friend'] = is_friend
    context['BASE_URL'] = settings.BASE_URL
    return render(request, "Accounts/account.html", context)



@login_required
def EditAccount(request, user_id):
    """
    update user info : take the FORM for the user creation and update through thse ones:
    UserCreationForm, PlatformUsersFormAll
    """
    try:
        user = User.objects.get(pk=user_id)
        userInfo = PlatformUsersAll.objects.get(user=user)
    except User.DoesNotExist and PlatformUsersAll.DoesNotExist:
        return HttpResponseRedirect(reverse('Accounts:signup'))
        
    #platformUser = PlatformUsersAll.objects.get(user=user)
    #print(platformUser)
    if request.method == "POST":
        userForm = UserCreationForm(request.POST, instance= user)
        userInfoForm = PlatformUsersFormAll(request.POST, instance=userInfo)
        
        if userForm.is_valid() and userInfoForm.is_valid() :
            user = userForm.save(commit=False) #don't save immediatley in DB , first put active = False
            #if user is a superuser, doesn't need to be activated; is supposed to be activated by default
            if user.is_superuser:
                user.save()
                user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
                user_info.user=user
                user_info.save() 
                messages.success(request, 'Your profile is updated successfully')
                return HttpResponseRedirect(reverse('Accounts:editProfile', user_id))  
            else:
                user.is_active = False 
                user.save() #save as unactive before email verification
                
                #Address and user_info must be saved, in any case if i delete user, delete everything else
                #address = addressForm.save()
                user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
                user_info.user=user
                #user_info.main_address = address #note : if you delete user/platformUser -> not delete address created          
                user_info.save() 
                #activation email is sent after the user complete the form
                activateEmail(request, user, userForm.cleaned_data.get('email')) #if the user SIGN-UP, compare this message: go to email and confirm + sent email
                messages.success(request, 'Your profile is updated successfully')
                return HttpResponseRedirect(reverse('Accounts:editProfile', user_id))    
    else:
        userForm = UserCreationForm(instance = user) #User auth connection
        userInfoForm = PlatformUsersFormAll(instance=userInfo) #user auth + added information
        
        #addressForm = AddressForm() #added information of address of User
        #'addressForm': addressForm
    return render(request, 'Accounts/account.html',  {'userForm': userForm, 'userInfoForm': userInfoForm})



'''
#DEBUG FUNCTION FOR LOG-IN
def user_login (request):
    
    if request.method =='POST':
        #get from dictionary, the name='username' filled in HTML form
        print((request.POST.get('username')))
        print((request.POST.get('password')))
        username = request.POST.get('username') 
        password = request.POST.get('password')
        #check if account is active
        user= authenticate(username=username, password=password) 
        print((user))
        if user: #not None
            #check if user still uses the service
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Core:categories_list'))
            else:
                messages.warning(request, 'Your account is not active.')
                return HttpResponseRedirect(reverse('Accounts:login'))
        else:
            print("Someone tried to login and failed!")
            print("Username : {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied")
    else :
        return render(request, 'Accounts/login.html')
    '''
    






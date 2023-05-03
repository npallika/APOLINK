from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory 
from django.contrib import messages
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from .forms import UserCreationForm, PlatformUsersFormAll, UserUpdateForm
#from .forms import UserCreationForm, PlatformUsersForm, AddressForm, PlatformUsersForm
from .models import PlatformUsersAll
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate
from django.utils.safestring import mark_safe
from django.utils.html import format_html


#EMAIL VERIFICATION view
def Activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) #take the PK of the user by decoding URL
        user = User.objects.get(pk=uid) #substituting the user from model with user from request
        print(f"USER FOUND {user} WITH PK = {uid} AND PASS = {user.password}")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
        print("User NOT FOUND")
    #if we found a current user saved (not actived yet) + check the token
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save() #now user, already saved before, is saved again, but ACTIVE!
        print(f"USER {vars(user)} HAS ACTIVE = {user.is_active}")
        messages.success(request, _("Thank you for your email confirmation. Now you can LOGIN in your account"))
        return HttpResponseRedirect(reverse('Accounts:login'))
    else:
        messages.error(request, _("Activation link is invalid!"))
    return HttpResponseRedirect(reverse('Core:categories_list'))


#send email function to activate new Users
def activateEmail(request, user, to_email):
    mail_subject = _('Activate your user account')
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
        msg = _('Dear <b>{username}</b>, please go to email <b>{to_email}</b> inbox and click on received activation link to confirm and complete the registration.<b> Note: </b>. Check your spam folder.')
        msg = format_html(msg, username =user.username, to_email=to_email)  # insert the translated variables into the message and mark it as safe
        messages.success(request, msg)  # show the translated message
        #successMex =  mark_safe(_(f'Dear <b>{user.username}</b>, please go to email <b>{to_email}</b> inbox and click on received activation link to confirm and complete the registration.<b> Note: </b>. Check your spam folder.'))
        #messages.success(request,successMex)
    else :
        messages.error(request, mark_safe(_(f'Problem sending email to {to_email}', 'check if you typed it correctly')))


#translation Test : useful to understand how translation works from views
def translate(language):
    cur_language = get_language()
    try:
        activate(language) #is not persistant
        text = _('hello')
    finally:
        activate(cur_language)
    #return text already translated
    return text

    
# pip install django-braces
def Signup(request):
    if request.method == "POST":
        userForm = UserCreationForm(request.POST)
        userInfoForm = PlatformUsersFormAll(request.POST)
        if userForm.is_valid()  and userInfoForm.is_valid() :
            user = userForm.save(commit=False) #don't save immediatley in DB , first put active = False
            #not yet activated, email verification first (activation) and don't set password!
            user.is_active = False 
            user.save() #save as unactive before email verification
            user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
            user_info.user=user        
            user_info.save() 
            
            #activation email is sent after the user complete the form
            activateEmail(request, user, userForm.cleaned_data.get('email')) #if the user SIGN-UP, compare this message: go to email and confirm + sent email
            return HttpResponseRedirect(reverse('Accounts:login'))  
    else:
        userForm = UserCreationForm() #User auth connection
        userInfoForm = PlatformUsersFormAll() #user auth + added information
    return render(request, 'accounts/signup.html', {'userForm': userForm, 'userInfoForm': userInfoForm})



@login_required
def user_logout(request):
    # Log out the user.
    messages.info(request, _("You have successfully logged out.")) 
    logout(request)
    # Return to homepage.
    return redirect("Core:categories_list")
    

class CustomLoginView(LoginView):
    #1) first is called with a GET : after clicking on email link
    #2) second is called with POST: user complete login form and is called again
    success_url = settings.LOGIN_REDIRECT_URL
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Access user's pk
            pk = user.pk
            # Perform login operation as usual
            messages.success(self.request, _('You have successfully logged in'))
            return super().form_valid(form)
        else:
            messages.warning(self.request, _('Your account is not active.'))
            #redirect('Accounts:login')
            return self.form_invalid(form)



@login_required
def AccountInfo(request, user_id):
    context={}
    try:
        user = User.objects.get(pk=user_id)
        print(f'the user is {user}')
        userInfo = PlatformUsersAll.objects.get(user=user)
        print(f'userInfo {userInfo}')
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
    user = request.user
    if user.is_authenticated and user != userInfo.user:
        is_self = False
    elif not user.is_authenticated:
        is_self = False
        
    # Set the template variables to the values : useful for letting other users seeing my profile and hide my email
    context['is_self'] = is_self
    context['BASE_URL'] = settings.BASE_URL
    return render(request, "Accounts/account.html", context)



@login_required
def EditAccount(request, user_id):
    """
    update user info : take the FORM for the user creation and update through these ones:
    UserCreationForm, PlatformUsersFormAll
    """
    try:
        #N.B. is more efficient take the user from the request , not directly from the model : less readings on the tables
        #user = User.objects.get(pk=user_id)
        user = request.user
        print(f'the request user is {user}')
        userInfo = PlatformUsersAll.objects.get(user=user)
        if not user.is_authenticated :
            return redirect('Accounts:login')
        if userInfo.user != request.user:
            return HttpResponse("You cannot edit someone elses profile.")
    except User.DoesNotExist and PlatformUsersAll.DoesNotExist:
        return HttpResponseRedirect(reverse('Accounts:signup'))   

    if request.method == "POST":
#<<<<<<< Updated upstream
        userForm = UserUpdateForm(request.POST, instance=user) #update = True
        userInfoForm = PlatformUsersFormAll(request.POST,  instance=userInfo) #request.FILES, if we want photos
#=======
#<<<<<<< Updated upstream
        #userForm = UserCreationForm(request.POST, instance= user) #update = True
        #userInfoForm = PlatformUsersFormAll(request.POST,  instance=userInfo) #request.FILES, if we want photos
        #print(userForm)
#=======
        #userForm = UserCreationForm(request.POST)
        #userInfoForm = PlatformUsersFormAll(request.POST)
        
#>>>>>>> Stashed changes
#>>>>>>> Stashed changes
        if userForm.is_valid() and userInfoForm.is_valid() :
            user = userForm.save(commit=False) #don't save immediatley in DB , first put active = False
            #if user is a superuser, doesn't need to be activated; is supposed to be activated by default:
            #so save the user without sending the activation email
            if user.is_superuser:
                user.save()
                user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
                user_info.user=user
                user_info.save() 
                messages.success(request, _('Your profile is updated successfully'))
                return HttpResponseRedirect(reverse('Accounts:login'))  
            else:
            #if user is not a superuser, activate it again , but just if it has modified something related his profile (userForm)
                if userForm.has_changed():
                    user.is_active = False 
                    user.save() #save as unactive before email verification
                    user_info = userInfoForm.save(commit=False) #don't save immediatley in DB
                    user_info.user=user        
                    user_info.save() 
                    #activation email is sent after the user complete the form and if cleaned data of userForms (old and new) are different
                    activateEmail(request, user, userForm.cleaned_data.get('email')) 
                    messages.success(request, _('Your profile is updated successfully'))
                else :
                    user_info = userInfoForm.save(commit=False) #don't save immediatley in DB (1-1 field)
                    user_info.user=user        
                    user_info.save() 
                    messages.success(request, _('Your profile is updated successfully'))
                return HttpResponseRedirect(reverse('Core:categories_list'))      
    else:
        userForm = UserUpdateForm(instance = user) #update=True : update : remove the possibility to change password here
        userInfoForm = PlatformUsersFormAll(instance=userInfo) #user auth + added information
        #if you want to set a MAX_MEMORY_SIZE for updated files , put this in the context + the forms and pass context variable
        #context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'Accounts/edit_account.html',  {'userForm': userForm, 'userInfoForm': userInfoForm})


class MyPasswordResetView(SuccessMessageMixin,PasswordResetView):
    template_name = "Accounts/password_reset/password_reset_form.html"
    email_template_name = "Accounts/password_reset/password_reset_email.html"
    subject_template_name = "Accounts/password_reset/password_reset_subject.txt"
    success_url = reverse_lazy ("Accounts:password_reset_done")




#DEBUG FUNCTION FOR LOG-IN
'''
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
    






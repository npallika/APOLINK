from django.urls import path, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

from . import views


app_name = 'Accounts'

urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    path('activate/<uidb64>/<token>', views.Activate, name ='activate'),
    path('accountInfo/<int:user_id>/', views.AccountInfo, name='account'),
    path('editAccount/<int:user_id>/', views.EditAccount, name='editAccount'),
    path('login/', views.CustomLoginView.as_view(template_name="Accounts/login.html"), name='login'),
    #path('login/', views.user_login, name='login'), #DEBUG
    path('logout/', views.user_logout, name='logout'),
    
    
    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='Accounts/password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='Accounts/password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy("Accounts:password_reset_complete")), name='password_reset_confirm'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
   ]
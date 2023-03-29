from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Accounts'

urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    path('activate/<uidb64>/<token>', views.Activate, name ='activate'),
    path('login/', views.CustomLoginView.as_view(template_name="Accounts/login.html"), name='login'),
    path('logout/', views.user_logout, name='logout'),
    #path('login/', views.CustomLoginView.as_view(template_name="Accounts/login.html"), name='login')
   ]
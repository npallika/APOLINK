from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Accounts'

urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name="signup"),
    path('signup/', views.Signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="Accounts/login.html"), name='login'),
    path('logout/', views.user_logout, name='logout'),
    #path("RegisterProduct/", views.CreateSellRent.as_view(), name="sellRent"),
    
]
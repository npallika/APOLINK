"""APOLINK2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

#put in urls patterns which path hasn't to have the prefix (en/el), and delte it from i18n_patterns() function
urlpatterns = [
    #path to redirect to the previous page after changing the language
    path("i18n/", include("django.conf.urls.i18n")),
    ]

#add at this function just the main paths you want to add the prefix to
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('Core.urls')),
    path('accounts/', include ('Accounts.urls')),
    path('Products/', include ('Products.urls')),
    path('captcha/', include('captcha.urls')),
    path('chaining/', include('smart_selects.urls')),
    #prefix_default_language = False : put as argument in i18n_patterns to remove prefix ('en' for example) for default language you setted in SETTINGS
)
#you can delete from urlpatterns and add directly to urlpatterns += i18n_patterns( path1 , path2, )


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

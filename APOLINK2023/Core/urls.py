from django.urls import path
from . import views

app_name = 'Core'

urlpatterns = [
    path('',views.CategoriesListView.as_view(),name='categories_list'),
    path('subcategories/<slug>', views.SubcategoriesListView.as_view(), name='subcategories'),
    
]
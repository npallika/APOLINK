from django.urls import path
from . import views

app_name = 'Products'

urlpatterns = [
    #path('<slug>', views.CategoriesProductsListView.as_view(), name='category_products_list'),
    path('<slug>', views.CategoriesProductsList, name='category_products_list'),
    #path('<int:pk>/Display', views.ProductDetails.as_view(), name='product_details'),
    path('Display/<int:pk>/', views.ProductSelected, name='product_details'),
    path('MyProductInfo/<int:pk>/', views.MyProductInfo, name='myProductInfo'),
    path('Create/<int:pk>/', views.ProductsSpecsCreate, name='technical_specs'),
    path('UpdateSpecs/<int:pk>/', views.ProductsSpecsUpdate, name='technical_specs_update'),
    path('RegisterProduct/', views.sell_rent, name='sellRent'),
    path('Search/', views.search_product, name='search_product'),
    path('My_Products/', views.show_my_products, name='show_my_products'),
    path('Delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('Update/<int:product_id>/', views.update_product, name='update_product'),
]
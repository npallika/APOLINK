from django.test import TestCase

# Create your tests here.

# Search feature
'''Create a form: Create a form that contains a search field. This form can be created using the Django forms framework.

View Function: Create a view function that handles the search request and performs the search. In the view function, you can access the search term from the form and use it to filter the products.

URL Configuration: Map the URL to the view function. You can do this by adding a new entry to the URL configuration in your Django project.

Template: Create a template that displays the search form and the results of the search. The template can use the Django template language to iterate over the filtered products and display them.

Deploy: Finally, deploy your application to a server to make it accessible to users. '''
# views.py
from django.shortcuts import render
from .models import Product
from .forms import ProductSearchForm

def search(request):
    form = ProductSearchForm(request.GET)
    products = Product.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        products = products.filter(name__contains=name)
    return render(request, 'search.html', {'form': form, 'products': products})

# forms.py
from django import forms

class ProductSearchForm(forms.Form):
    name = forms.CharField(label='Search by name')

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    # ... other url patterns
]

# search.html
<form method="get">
  {{ form.as_p }}
  <input type="submit" value="Search">
</form>

{% if products %}
  <ul>
    {% for product in products %}
      <li>{{ product.name }}</li>
    {% endfor %}
  </ul>
{% else %}
  <p>No products found</p>
{% endif %}

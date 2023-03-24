import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import FirstLevelCategories, SecondLevelCategories
from Products.models import ThirdLevelCategories
from django.views.generic import (ListView,
                                  DetailView)
# Create your views here.


class CategoriesListView(ListView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('Core:categories_list')
    
    queryset = FirstLevelCategories.objects.order_by('name')
    context_object_name = 'FirstLevelCategories'
    template_name = 'Core/maincategories_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SecondLevelCategories'] = SecondLevelCategories.objects.all()
        context['searchable'] = ThirdLevelCategories.objects.all()
        return context

    

class SubcategoriesListView(DetailView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('Core:categories_list')
    
    context_object_name = 'product_subcategories'
    model = SecondLevelCategories
    template_name = 'Core/subcategories_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs["object"])
        context['Subcategories'] = ThirdLevelCategories.objects.filter(parent_cat = kwargs["object"])
        return context




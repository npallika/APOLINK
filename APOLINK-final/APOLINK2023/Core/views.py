from django.shortcuts import render
from .models import FirstLevelCategories, SecondLevelCategories
from Products.models import ThirdLevelCategories
from django.views.generic import (ListView,DetailView)
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate

# Create your views here.

class CategoriesListView(ListView):
    queryset = FirstLevelCategories.objects.order_by('name')
    context_object_name = 'FirstLevelCategories'
    template_name = 'Core/maincategories_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SecondLevelCategories'] = SecondLevelCategories.objects.all()
        context['searchable'] = ThirdLevelCategories.objects.all()
        return context

class SubcategoriesListView(DetailView):
    
    context_object_name = 'product_subcategories'
    model = SecondLevelCategories
    template_name = 'Core/subcategories_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Subcategories'] = ThirdLevelCategories.objects.filter(parent_cat = kwargs["object"])
        return context



def categories_list(request, slug):
      
    print(f"The slug is {slug}")
    main_category = FirstLevelCategories.objects.get(slug=slug)
    print(f"The main category is {main_category.name}")
    sub_categories = SecondLevelCategories.objects.filter(parent_cat=main_category)
    for sub in sub_categories:
        print(f"The subcategory is {sub.name}")
    
    third_level_categories = ThirdLevelCategories.objects.filter(parent_cat__in = sub_categories)
    for third in third_level_categories:
        print(f"The third level categories is {third}")

    return render(request, 'Core/categories_list.html', {'category':main_category, 'subcategories':sub_categories, 'thirdlevelcategories':third_level_categories})


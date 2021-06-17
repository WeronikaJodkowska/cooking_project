from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Category, Ingredient


class CategoryListView(ListView):
    model = Category
    template_name = 'ingredients/categories/category_list.html'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'ingredients/categories/category_detail.html'


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient/ingredient_list.html'

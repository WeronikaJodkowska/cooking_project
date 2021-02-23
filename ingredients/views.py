from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Ingredient


# def ingredient_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     ingredients = Ingredient.objects.all()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         ingredients = ingredients.filter(category=category)
#     return render(request,
#                   'ingredients/ingredient/list.html',
#                   {'category': category,
#                    'categories': categories,
#                    'ingredients': ingredients})


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


# class IngredientDetailView(DetailView):
#     model = Ingredient
#     context_object_name = 'ingredient'
#     template_name = 'ingredients/ingredient/recipe_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category_id'] = self.kwargs.get('pk')
#         return context


class SearchResultsListView(ListView):
    model = Ingredient
    context_object_name = 'ingredient_list'
    template_name = 'ingredients/ingredient/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Ingredient.objects.filter(
            Q(name__icontains=query)
        )

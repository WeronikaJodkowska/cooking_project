from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Recipe


def recipe_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        recipes = recipes.filter(category=category)
    return render(request,
                  'recipes/recipe/recipe_list.html',
                  {'category': category,
                   'categories': categories,
                   'recipes': recipes})


def recipe_detail(request, id, slug):
    recipe = get_object_or_404(Recipe,
                               id=id,
                               slug=slug)
    return render(request,
                  'recipes/recipe/detail.html',
                  {'recipe': recipe})


class CategoryListView(ListView):
    model = Category
    template_name = 'recipes/categories/category_list.html'

    # def get_queryset(self):
    #     return Recipe.objects.filter(category_id=self.kwargs.get('pk'))

# class RecipeByCategoryListView(ListView):
#     model = Category
#     template_name = 'recipes/recipe/recipe_by_category.html'
#     context_object_name = 'category'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category, name=self.kwargs['category'])
#         return Recipe.objects.filter(category=self.category)
#
#     def get_context_data(self, **kwargs):
#         context = super(RecipeByCategoryListView, self).get_context_data(**kwargs)
#         context['category'] = self.category
#         return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'recipes/categories/category_detail.html'

    # def get_queryset(self):
    #     return Recipe.objects.filter(category_id=self.kwargs.get('pk'))

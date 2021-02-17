from django.shortcuts import render, get_object_or_404

from .models import Category, Recipe


def recipe_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        recipes = recipes.filter(category=category)
    return render(request,
                  'recipes/recipe/list.html',
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

from django.shortcuts import render, get_object_or_404

from .models import Category, Ingredient


def ingredient_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        ingredients = ingredients.filter(category=category)
    return render(request,
                  'ingredients/ingredient/list.html',
                  {'category': category,
                   'categories': categories,
                   'ingredients': ingredients})



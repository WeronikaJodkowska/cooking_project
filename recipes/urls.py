"""cooking_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import CategoryListView, CategoryDetailView, RecipeListView, \
    SearchResultsListView, CreateRecipeView, IngredientAutoComplete, \
    RecipeByUserView, RecipeOwnView, RecipeDetailView, RecipeByTimeView, \
    CategoryAutoComplete, RecipeByIngredient

app_name = 'recipes'

urlpatterns = [
    path('account/', include('account.urls')),
    path('recipes/', CategoryListView.as_view(), name='category_list'),
    path('recipes_by_user/<int:pk>', RecipeByUserView.as_view(), name='recipes_by_user'),
    path('recipes_own/<int:pk>', RecipeOwnView.as_view(), name='recipes_own'),
    path('recipes_by_time/<int:pk>', RecipeByTimeView.as_view(), name='recipes_by_time'),
    path('recipes_by_ingredient/<int:pk>', RecipeByIngredient.as_view(), name='recipes_by_ingredient'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>', RecipeDetailView.as_view(), name='recipe_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('recipe/new/', CreateRecipeView.as_view(), name='recipe_new'),
    path('category-autocomplete/', CategoryAutoComplete.as_view(), name='category-autocomplete'),
    path('ingredient_autocomplete/', IngredientAutoComplete.as_view(), name='ingredient_autocomplete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


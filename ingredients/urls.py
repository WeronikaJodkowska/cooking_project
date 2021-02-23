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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CategoryListView, CategoryDetailView, IngredientListView, SearchResultsListView

app_name = 'ingredients'

urlpatterns = [
    # path('', views.ingredient_list, name='ingredient_list'),
    # path('<slug:category_slug>/', views.ingredient_list,
    #      name='ingredient_list_by_category'),
    path('account/', include('account.urls')),
    path('recipes/', include('recipes.urls')),

    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
    path('search/', SearchResultsListView.as_view(), name='ingredient_search_results'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from . import views
from .views import CategoryListView, CategoryDetailView

app_name = 'recipes'

urlpatterns = [
    # path('', views.recipe_list, name='recipe_list'),
    # path('<slug:category_slug>/', views.recipe_list,
    #      name='recipe_list_by_category'),
    # path('<int:id>/<slug:slug>/', views.recipe_detail,
    #      name='recipe_detail'),

    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.autocomplete, name='autocomplete'),
    path('account', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('edit/', views.edit, name='edit'),
    path('favrecipe/<int:id>/', views.favourite_recipe_add, name='favourite_recipe_add'),
    path('favrecipes/', views.favourite_recipe_list, name='favourite_recipe_list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

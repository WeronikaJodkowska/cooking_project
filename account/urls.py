from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from ingredients import views as ingredients_views

app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # change password urls
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    # path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', views.dashboard, name='dashboard'),
    # path('ingredients/', include("ingredients.urls")),
    # path('', ingredients_views.ingredient_list, name='ingredient_list'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('favrecipe/<int:id>/', views.favourite_recipe_add, name='favourite_recipe_add'),
    path('favrecipes/', views.favourite_recipe_list, name='favourite_recipe_list'),
    path('favingredient/<int:id>/', views.favourite_ingredient_add, name='favourite_ingredient_add'),
    path('favingredients/', views.favourite_ingredient_list, name='favourite_ingredient_list'),
    path('cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list, name='cart_list'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

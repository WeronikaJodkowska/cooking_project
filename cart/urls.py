from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from cart.views import CartCreate as cart_views
from . import views
from .views import CreateCart

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='list'),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete/<str:pk>/', views.deleteTask, name="delete_task"),

    path('cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list, name='cart_list'),
    # path('cart/<int:id>/', CreateCartView.as_view(), name='cart_new'),
    # path('cart/add', views.CartCreate.as_view(), name='cart_add'),
    path('cart/add', CreateCart.as_view(), name='cart_add'),

    path('cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list, name='cart_list'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



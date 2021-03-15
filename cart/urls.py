from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='list'),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete/<str:pk>/', views.deleteTask, name="delete_task"),

    path('cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:id>/', views.delete_from_cart, name='delete_from_cart'),
    path('cart/', views.cart_list, name='cart_list'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

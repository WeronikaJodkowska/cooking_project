from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import CategoryListView, CategoryDetailView, DiseaseListView, \
    DiseaseDetailView, CreateBlacklist, PostBlacklist
from . import views

app_name = 'diseases'

urlpatterns = [

    path('account/', include('account.urls')),
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('disease/', DiseaseListView.as_view(), name='disease_list'),
    path('disease/<int:pk>', DiseaseDetailView.as_view(), name='disease_detail'),
    path('blacklist/', views.black_list, name='black_list'),

    # path('blacklist/new', CreateBlacklist.as_view(), name='blacklist_new'),
    # path('blacklist/new', PostBlacklist.as_view(), name='blacklist_new'),
    path('blacklist/<int:id>/', views.add_to_blacklist, name='add_to_blacklist'),
    path('blacklist/delete/<int:id>/', views.delete_from_blacklist, name='delete_from_blacklist'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import CategoryListView, CategoryDetailView, DiseaseListView, DiseaseDetailView

app_name = 'diseases'

urlpatterns = [

    path('account/', include('account.urls')),
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('disease/', DiseaseListView.as_view(), name='disease_list'),
    path('disease/<int:pk>', DiseaseDetailView.as_view(), name='disease_detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


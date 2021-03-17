from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify

from .models import Category, Disease


class CategoryListView(ListView):
    model = Disease
    template_name = 'diseases/categories/category_list.html'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'diseases/categories/category_detail.html'


class DiseaseListView(ListView):
    model = Disease
    template_name = 'diseases/disease/disease_list.html'

    # def get_queryset(self):
    #     return Disease.objects.filter(status='p')


class DiseaseDetailView(DetailView):
    model = Disease
    context_object_name = 'disease'
    template_name = 'diseases/disease/disease_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('pk')
        return context

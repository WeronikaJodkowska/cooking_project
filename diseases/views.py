from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify

from .models import Category, Disease, BlackList
from .forms import BlackListCreateForm


class CategoryListView(ListView):
    model = Category
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


class CreateBlacklist(LoginRequiredMixin, CreateView):
    model = BlackList
    form_class = BlackListCreateForm
    template_name = 'diseases/blacklist/blacklist_create.html'
    success_url = "/diseases"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def get_queryset(self):
    #     self.disease = get_object_or_404(Disease, name=self.kwargs['disease'])
    #     return Book.objects.filter(disease=self.disease)

    def form_valid(self, form):
        # messages.success(self.request, 'form is valid')
        form.instance.user = self.request.user
        # form.instance.disease = self.kwargs['Disease.id']
        form.save()
        return super(CreateBlacklist, self).form_valid(form)

# class CreateBlacklist(CreateView):
#     model = BlackList
#     # form_class = BlackListCreateForm
#     fields = '__all__'
#     template_name = 'diseases/blacklist/blacklist_create.html'
#     success_url = "/diseases"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         disease = get_object_or_404(Disease, id=id)
#         context["disease_ingredients"] = disease.list_ingredient.all()
#         return context

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.user = request.user
#         return super(CreateBlacklist, self).form_valid(form)
# class CreateRecipeView(CreateView):
#     model = Recipe
#     form_class = RecipeCreateForm
#     template_name = 'recipes/recipe/recipe_create.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(CreateRecipeView, self).form_valid(form)


@login_required
def black_list(request):
    # cart = Cart.objects.all().filter(user=request.user)
    blacklist = BlackList.objects.filter(user=request.user)
    return render(request,
                  'diseases/blacklist/blacklist.html',
                  {'blacklist': blacklist})


# @login_required
# def add_to_blacklist(request, id):
#     # disease = get_object_or_404(Disease, id=id)
#     disease = Disease.objects.get(id=id)
#
#     user = get_object_or_404(User, id=request.user.id)
#     if not BlackList.objects.all().filter(disease=disease).exists():
#
#         blacklist = BlackList(user=user)
#         blacklist.save()
#         # blacklist.disease.set(disease)
#
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_to_blacklist(request, id):
    disease = get_object_or_404(Disease, id=id)
    user = get_object_or_404(User, id=request.user.id)

    # if not BlackList.objects.all().filter(disease=disease).exists():
    cart = BlackList(user=user)
    cart.save()
    cart.disease.add(disease)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify

from .models import Category, Recipe
from .forms import RecipeCreateForm


# def recipe_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     recipes = Recipe.objects.all()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         recipes = recipes.filter(category=category)
#     return render(request,
#                   'recipes/recipe/recipe_list.html',
#                   {'category': category,
#                    'categories': categories,
#                    'recipes': recipes})
#
#
# def recipe_detail(request, id, slug):
#     recipe = get_object_or_404(Recipe,
#                                id=id,
#                                slug=slug)
#     return render(request,
#                   'recipes/recipe/recipe_detail.html',
#                   {'recipe': recipe})


class CategoryListView(ListView):
    model = Category
    template_name = 'recipes/categories/category_list.html'

    # def get_queryset(self):
    #     return Recipe.objects.filter(category_id=self.kwargs.get('pk'))


# class RecipeByCategoryListView(ListView):
#     model = Category
#     template_name = 'recipes/recipe/recipe_by_category.html'
#     context_object_name = 'category'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category, name=self.kwargs['category'])
#         return Recipe.objects.filter(category=self.category)
#
#     def get_context_data(self, **kwargs):
#         context = super(RecipeByCategoryListView, self).get_context_data(**kwargs)
#         context['category'] = self.category
#         return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'recipes/categories/category_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['status'] = self.kwargs.get('p')
    #     return context
    # def get_queryset(self):
    #     return Recipe.objects.filter(status='Published')
    # def get_queryset(self):
    #     return Recipe.objects.filter(category_id=self.kwargs.get('pk'))


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_list.html'

    def get_queryset(self):
        return Recipe.objects.filter(status='p')


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('pk')
        # context['list_ingredient'] = self.kwargs.get('pk')
        return context

    # def get_queryset(self):
    #     return Recipe.objects.prefetch_related('list_ingredient')


class SearchResultsListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Recipe.objects.filter(
            Q(name__icontains=query)
        )


# def recipe_new(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             recipe.save()
#             return redirect('recipes:recipe_detail', pk=recipe.pk)
#     else:
#         form = RecipeForm()
#     return render(request,
#                   'recipes/recipe/recipe_create.html',
#                   {'form': form})


class CreateRecipeView(CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipes/recipe/recipe_create.html'
    success_url = '/'
    success_message = 'Ваш рецепт на рассмотрении.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        # if form.is_valid():
        #     messages.success('Profile updated successfully')
        # else:
        #     messages.error('Error updating your profile')
        return super(CreateRecipeView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class SuccessDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_created.html'

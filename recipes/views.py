import re
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchQuery
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import ListView, DetailView, CreateView

from diseases.models import BlackList, Disease
from .forms import *
from .models import RecipeCategory, Recipe, Direction, RecipeIngredients


def filter_text(self, queryset, name, value):
    """Full-text search."""
    query = SearchQuery(value, config="simple")
    return (
        queryset.filter(**{name: query})
            # This assumes that field is already a TextSearch vector and thus
            # doesn't need to be transformed. To achieve that F function is
            # required.
            # .annotate(rank=SearchRank(F(name), query)).order_by("-rank")
            .filter(status='p')
    )


class CategoryListView(ListView):
    model = RecipeCategory
    context_object_name = 'category_list'
    template_name = 'recipes/categories/category_list.html'


class CategoryDetailView(DetailView):
    model = RecipeCategory
    context_object_name = 'category'
    template_name = 'recipes/categories/category_detail.html'


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_list.html'
    paginate_by = 10

    def get_queryset(self):
        try:
            entry = Recipe.objects.filter(status='p')
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = RecipeCategory.objects.all()
        context['all_colleges'] = Ingredient.objects.all()
        return context


class CategoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RecipeCategory.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe/recipe_detail.html'
    qs = RecipeCategory.objects.values_list('name', flat=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = RecipeCategory.objects.all()
        favorites = get_object_or_404(Recipe, id=self.kwargs['pk'])
        favorited = False
        if favorites.favourites.filter(id=self.request.user.id).exists():
            favorited = True
        context['recipe_is_favorited'] = favorited
        context['list_ingredient'] = RecipeIngredients.objects.filter(recipe_id=self.kwargs.get('pk'))
        context['directions'] = Direction.objects.filter(recipe_id=self.kwargs.get('pk'))
        ingredients = RecipeIngredients.objects.filter(recipe=self.kwargs.get('pk'))
        recipe_ingredients = []
        disease_ingredients = []
        d_o = []
        for i in ingredients:
            recipe_ingredients.append(i.ingredient.name)
        if self.request.user.is_authenticated:
            context['blacklist'] = BlackList.objects.filter(user=self.request.user)
            context['diseases'] = Disease.objects.filter(blacklist_disease__user=self.request.user)
            diseases = Disease.objects.filter(blacklist_disease__user=self.request.user)
            for disease in diseases.distinct():
                disease_ingr = disease.list_ingredient.all().filter()
                d_i = {disease: disease_ingr}
                d_o.append(d_i)
                for i in disease_ingr:
                    disease_ingredients.append(i.name)
            same_ingredients = list(set(recipe_ingredients) & set(disease_ingredients))
            context['disease_ingredient'] = same_ingredients
            context['disease_name'] = diseases.values_list('name').distinct()
        return context


class SearchResultsListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        result = super(SearchResultsListView, self).get_queryset()
        q = self.request.GET.get('q')
        q1 = self.request.GET.get('q1')
        q = re.split(', ', q)
        q1 = re.split(', ', q1)
        if q != ['']:
            recipe_object = RecipeIngredients.objects.filter(
                Q(ingredient__name__in=q)).prefetch_related().distinct().values_list('recipe', flat=True)
            if q1:
                recipe_except = recipe_object.exclude(Q(ingredient__name__in=q1))
                result = Recipe.objects.filter(pk__in=recipe_except)
        elif q == ['']:
            recipe_object = RecipeIngredients.objects.filter(recipe__status='p')\
                .prefetch_related().distinct().values_list('recipe', flat=True)
            if q1:
                ingredient_names = recipe_object.filter(Q(ingredient__name__in=q1))
                recipe_except = recipe_object.difference(ingredient_names)
                result = Recipe.objects.filter(pk__in=recipe_except)
        else:
            result = None
        return result


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipes/recipe/recipe_create.html'
    success_message = 'Ваш рецепт на рассмотрении.'

    def get_context_data(self, **kwargs):
        context = super(CreateRecipeView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['directions'] = RecipeDirectionFormSet(self.request.POST, self.request.FILES)
            context['ingredients'] = RecipeIngredientsFormSet(self.request.POST)
        else:
            context['directions'] = RecipeDirectionFormSet()
            context['ingredients'] = RecipeIngredientsFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        recipe = self.kwargs.get('pk')
        directions = context['directions']
        ingredients = context['ingredients']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if directions.is_valid():
                directions.instance = self.object
                directions.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        messages.success(self.request, mark_safe("Your recipe has been successfully added and is being verified by the "
                                                 "administrator. <br/>Once it is checked, it can be found in your "
                                                 "profile in My recipes. Thank you!"))
        return super(CreateRecipeView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_success_url(self):
        return reverse_lazy('recipes:recipe_detail', kwargs={'pk': self.object.pk})


class SuccessDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_created.html'


class IngredientAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Ingredient.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class RecipeByUserView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_by_user.html'

    def get_queryset(self):
        try:
            entry = Recipe.objects.filter(user=self.kwargs.get('pk'), status='p')
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry


class RecipeOwnView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_own.html'

    def get_queryset(self):
        try:
            entry = Recipe.objects.filter(user=self.request.user, status='p')
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry


class RecipeByTimeView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_by_time.html'

    def get_queryset(self):
        try:
            recipe_id = self.kwargs.get('pk')
            time = Recipe.objects.values('preparation_time').filter(id=recipe_id)
            entry = Recipe.objects.filter(preparation_time__in=time, status='p')
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry


class RecipeByMeasurementView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        result = super(RecipeByMeasurementView, self).get_queryset()
        q = self.request.GET.get('q')
        q = re.split(' |;|; |, |,|\*|\n', q)
        if q:
            postresult = Recipe.objects.filter(Q(list_ingredient__name__in=q)).prefetch_related().distinct()
            result = postresult
        else:
            result = None
        return result


class RecipeByIngredient(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_by_ingredient.html'

    def get_queryset(self):
        result = super(RecipeByIngredient, self).get_queryset()
        ingredient = self.kwargs.get('pk')
        ingredient_name = Ingredient.objects.values('name').filter(id=ingredient)
        print(ingredient)
        print(ingredient_name)
        recipe_object = RecipeIngredients.objects.filter(ingredient__name__in=ingredient_name).\
            prefetch_related().distinct().values_list('recipe', flat=True)
        print(recipe_object)
        result = Recipe.objects.filter(pk__in=recipe_object)
        print(result)
        # result = Recipe.objects.filter(Q(list_ingredient__name__in=q)).prefetch_related().distinct()
        return result
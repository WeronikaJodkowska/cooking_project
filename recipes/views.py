import re
from dal import autocomplete
from django.contrib import messages
from django.contrib.postgres.search import SearchQuery
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from more_itertools import unique_everseen

from diseases.models import BlackList, Disease
from ingredients.models import Ingredient
from .forms import RecipeCreateForm
from .models import Category, Recipe, Direction, RecipeIngredients


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
    model = Category
    template_name = 'recipes/categories/category_list.html'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    # paginate_by = 2
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


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_ingredient'] = RecipeIngredients.objects.filter(recipe_id=self.kwargs.get('pk'))
        context['directions'] = Direction.objects.filter(recipe_id=self.kwargs.get('pk'))
        ingredients = RecipeIngredients.objects.filter(recipe=self.kwargs.get('pk'))
        print('ingredients ', ingredients)
        for i in ingredients:
            print(i.amount, i.unit.name, i.ingredient.name)
        directions = Direction.objects.filter(recipe_id=self.kwargs.get('pk'))
        print('direction', directions)
        for d in directions:
            print(d.text)

        # if self.request.user.is_authenticated:
        #     global i_1, i_2, i_3, i_4
        #     context = super().get_context_data(**kwargs)
        #     context['directions'] = Direction.objects.filter(recipe_id=self.kwargs.get('pk'))
        #     context['blacklist'] = BlackList.objects.filter(user=self.request.user)
        #     context['diseases'] = Disease.objects.filter(blacklist_disease__user=self.request.user)
        #     recipes = Recipe.objects.filter(pk=self.kwargs.get('pk'))
        #     diseases = Disease.objects.filter(blacklist_disease__user=self.request.user)
        #
        #     same_ingredients = []
        #     res_diseases = []
        #     dis_ingr = {}
        #     res_dis_ingr = []
        #     for disease in diseases:
        #         disease_ingr = disease.list_ingredient.all()
        #         print("disease_ingr:", disease_ingr)
        #         for recipe in recipes:
        #             recipe_ingr = recipe.list_ingredient.all()
        #             print("recipe_ingr:", recipe_ingr)
        #             same = list(set(disease_ingr) & set(recipe_ingr))
        #             print("same ", same)
        #             same_ingredients.append(same)
        #             print("same_ingredients ", same_ingredients)
        #             dis_ingr = {disease: same}
        #             print("dis_ingr ", dis_ingr)
        #             res_dis_ingr.append(dis_ingr)
        #             print("res_dis_ingr ", res_dis_ingr)
        #             for i in same_ingredients:
        #                 for j in i:
        #                     res_diseases.append(str(j))
        #                     print("res_diseases ", res_diseases)
        #
        #     print(same_ingredients)
        #     result = list(unique_everseen(res_diseases))
        #     print("res_disease: ", result)
        #     print("res_dis_ingr: ", res_dis_ingr)
        #     # for i in res_dis_ingr:
        #     #     print("keys ", i.keys())
        #     #     for j in i:
        #     #         print("j ", j)
        #     #         print("values ", i.values())
        #     #         for k in i.values():
        #     #             if len(k) == 0:
        #     #                 print("0")
        #     #             else:
        #     #                 print("k ", k)
        #     #             for g in k:
        #     #                 print(g)
        #     context['same'] = result
        #     context['disease_ingredient'] = res_dis_ingr
        return context


class SearchResultsListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        result = super(SearchResultsListView, self).get_queryset()
        q = self.request.GET.get('q')
        q = re.split(' |;|; |, |,|\*|\n', q)
        # for i in range(len(q)):
        #     print(q[i])
        if q:
            postresult = Recipe.objects.filter(Q(list_ingredient__name__in=q)).prefetch_related().distinct()
            result = postresult
        else:
            result = None
        return result


class CreateRecipeView(CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipes/recipe/recipe_create.html'
    success_url = '/'
    success_message = 'Ваш рецепт на рассмотрении.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        recipe = self.kwargs.get('pk')
        print(recipe)
        # if not Direction.objects.all().filter(recipe=self.kwargs.get('pk')).exists():
        #     recipe = get_object_or_404(Recipe, id=id)
        #     print(self.kwargs.get('pk'))
        #     form.instance.direction = direction

        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return super(CreateRecipeView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


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
            entry = Recipe.objects.filter(user=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry


class RecipeOwnView(ListView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_own.html'

    def get_queryset(self):
        try:
            entry = Recipe.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry

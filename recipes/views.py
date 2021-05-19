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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = RecipeCategory.objects.all()
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
    print(qs)

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
        # print('ingredients ', ingredients)
        recipe_ingredients = []
        disease_ingredients = []
        same_ingredients = []
        disease_name = []
        for i in ingredients:
            recipe_ingredients.append(i.ingredient.name)
        # print(recipe_ingredients)

        # directions = Direction.objects.filter(recipe_id=self.kwargs.get('pk'))
        # print('direction', directions)
        # for d in directions:
        #     print(d.text)
        if self.request.user.is_authenticated:
            context['blacklist'] = BlackList.objects.filter(user=self.request.user)
            context['diseases'] = Disease.objects.filter(blacklist_disease__user=self.request.user)
            diseases = Disease.objects.filter(blacklist_disease__user=self.request.user)
            for disease in diseases:
                disease_ingr = disease.list_ingredient.all().filter()
                for i in disease_ingr:
                    disease_ingredients.append(i.name)

            # print(disease_ingredients)
            same_ingredients = list(set(recipe_ingredients) & set(disease_ingredients))
            print(same_ingredients)

            context['disease_ingredient'] = same_ingredients
            context['disease_name'] = disease_name
            # print(disease_name)
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
        # print(context['disease_ingredient'])
        return context


class SearchResultsListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        result = super(SearchResultsListView, self).get_queryset()
        q = self.request.GET.get('q')
        q = re.split(' |;|; |, |,|\*|\n', q)
        recipe_id = []
        # for i in range(len(q)):
        #     print(q[i])
        if q:
            recipe_object = RecipeIngredients.objects.filter(
                Q(ingredient__name__in=q)).prefetch_related().distinct().values_list('recipe', flat=True)
            print(q)
            print(recipe_object)
            # for r in recipe_object:
            #     recipe_id.append(r)
            # print(recipe_id[0])

            result = Recipe.objects.filter(pk__in=recipe_object)
            print(result)
            # recipe = Recipe.objects.get(pk__in=recipe_id)
            # print(recipe.name)
            # postresult = Recipe.objects.filter(Q(list_ingredient__name__in=q)).prefetch_related().distinct()
        #     result = recipe
        else:
            result = None
        return result


# class SearchResultsListView(ListView):
#     model = Recipe
#     context_object_name = 'recipe_list'
#     template_name = 'recipes/recipe/search_results.html'
#
#     def get_queryset(self):
#         result = super(SearchResultsListView, self).get_queryset()
#         keywords = self.request.GET.get('q')
#         keywords = re.split(' |;|; |, |,|\*|\n', q)
#         recipe_id = []
#         # for i in range(len(q)):
#         #     print(q[i])
#         if keywords:
#             qs = [Q()]
#             recipe_object = RecipeIngredients.objects.filter(
#                 Q(ingredient__name__in=q)).prefetch_related().distinct().values_list('recipe', flat=True)
#             print(q)
#             print(recipe_object)
#             # for r in recipe_object:
#             #     recipe_id.append(r)
#             # print(recipe_id[0])
#
#             result = Recipe.objects.filter(pk__in=recipe_object)
#             print(result)
#             # recipe = Recipe.objects.get(pk__in=recipe_id)
#             # print(recipe.name)
#             # postresult = Recipe.objects.filter(Q(list_ingredient__name__in=q)).prefetch_related().distinct()
#         #     result = recipe
#         else:
#             result = None
#         return result


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipes/recipe/recipe_create.html'
    # success_url = '/'
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
            print(self.object)
            if directions.is_valid():
                directions.instance = self.object
                directions.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        # if not Direction.objects.all().filter(recipe=self.kwargs.get('pk')).exists():
        #     recipe = get_object_or_404(Recipe, id=id)
        #     print(self.kwargs.get('pk'))
        #     form.instance.direction = direction
        messages.success(self.request, mark_safe("Your recipe has been successfully added and is being verified by the "
                                                 "administrator. <br/>Once it is checked, it can be found in your "
                                                 "profile in My recipes. Thank you!"))
        # success_message = self.get_success_message(form.cleaned_data)
        # if success_message:
        #     messages.success(self.request, success_message)
        return super(CreateRecipeView, self).form_valid(form)


    # def get_form(self, form_class=None):
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
            entry = Recipe.objects.filter(user=self.kwargs.get('pk'))
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
            recipe = Recipe.objects.filter(id=recipe_id)
            time = Recipe.objects.values('preparation_time').filter(id=recipe_id)
            print(time)
            entry = Recipe.objects.filter(preparation_time__in=time)
            print(entry)
            unit = RecipeIngredients.objects.filter(unit__name='g')
            print('unit ', unit)
            recipe_unit = RecipeIngredients.objects.filter(ingredient__name__istartswith='Мука').filter(
                unit__name='g').filter(amount='100').values('recipe')
            print(recipe_unit)
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

# class CreateRecipeView(CreateView):
#     form_class = RecipeCreateForm
#     template_name = 'recipes/recipe/recipe_create.html'
#     model = Recipe
#     success_url = '/'
#
#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         direction_form = DirectionFormSet()
#         direction_formhelper = DirectionFormHelper()
#
#         return self.render_to_response(
#             self.get_context_data(form=form, direction_form=direction_form))
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         direction_form = DirectionFormSet(self.request.POST)
#
#         if form.is_valid() and direction_form.is_valid():
#             return self.form_valid(form, direction_form)
#
#         return self.form_invalid(form, direction_form)
#
#     def form_valid(self, form, direction_form):
#         """
#         Called if all forms are valid. Creates a Author instance along
#         with associated books and then redirects to a success page.
#         """
#         self.object = form.save()
#         direction_form.instance = self.object
#         direction_form.save()
#
#     def form_invalid(self, form, direction_form):
#         """
#         Called if whether a form is invalid. Re-renders the context
#         data with the data-filled forms and errors.
#         """
#         return self.render_to_response(
#             self.get_context_data(form=form, direction_form=direction_form)
#         )
#
#     def get_context_data(self, **kwargs):
#         """ Add formset and formhelper to the context_data. """
#         ctx = super(CreateRecipeView, self).get_context_data(**kwargs)
#         direction_formhelper = DirectionFormHelper()
#
#         if self.request.POST:
#             ctx['form'] = RecipeCreateForm(self.request.POST)
#             ctx['direction_form'] = DirectionFormSet(self.request.POST)
#             ctx['direction_formhelper'] = direction_formhelper
#         else:
#             ctx['form'] = RecipeCreateForm()
#             ctx['direction_form'] = DirectionFormSet()
#             ctx['direction_formhelper'] = direction_formhelper
#
#         return ctx


# def create_recipe(request):
#     RecipeFormSet = inlineformset_factory(Recipe, Direction, fields=('text', 'image'), extra=3)
#     form = RecipeCreateForm(request.POST or None, request.FILES or None)
#     formset = RecipeFormSet(request.POST or None, request.FILES or None)
#
#     if form.is_valid() and formset.is_valid():
#         recipe = form.save()
#         for form in formset.forms:
#             direction = form.save(commit=False)
#             direction.recipe = recipe
#             direction.save()
#     # return HttpResponseRedirect(reverse('recipes:recipe_new'))
#     return render(request, 'recipes/recipe/recipe_create.html', {'form': form, 'formset': formset})

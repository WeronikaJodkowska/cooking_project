from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from .models import Category, Recipe
from .forms import RecipeCreateForm

from diseases.models import BlackList, Disease

from ingredients.models import Ingredient


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
    # paginate_by = 2
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
    paginate_by = 10

    def get_queryset(self):
        try:
            entry = Recipe.objects.filter(status='p')
        except ObjectDoesNotExist:
            print("Either the Recipe or entry doesn't exist.")
        return entry


class RecipeDetailNotLoggedView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe/recipe_detail.html'


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe/recipe_detail.html'

    # def get_queryset(self, **kwargs):
    #     global i_1, i_2, i_3
    #     recipes = Recipe.objects.filter(pk=self.kwargs.get('pk'))
    #     print(recipes)
    #     diseases = Disease.objects.filter(blacklist_disease__user=self.request.user)
    #     print(diseases)
    #     for recipe in recipes:
    #         i_1 = recipe.list_ingredient.all()
    #         print(i_1)
    #     for disease in diseases:
    #         i_2 = disease.list_ingredient.all()
    #         print("2: ", i_2)
    #         i_3 = i_2.intersection(i_1)
    #         print(i_3)
    #     return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_ingredient'] = self.kwargs.get('pk')
        if self.request.user.is_authenticated:
            global i_1, i_2, i_3, i_4
            context = super().get_context_data(**kwargs)
            # context['list_ingredient'] = self.kwargs.get('pk')
            context['blacklist'] = BlackList.objects.filter(user=self.request.user)
            context['diseases'] = Disease.objects.filter(blacklist_disease__user=self.request.user)
            recipes = Recipe.objects.filter(pk=self.kwargs.get('pk'))
            diseases = Disease.objects.filter(blacklist_disease__user=self.request.user)
        # i_3 = i_2.intersection(i_1)
        # for recipe in recipes:
        #     i_1 = recipe.list_ingredient.all()
        #     print("1. recipe_ingredients: ", i_1)
        #     for disease in diseases:
        #         i_2 = disease.list_ingredient.all()
        #         print("2. disease_ingredients: ", i_2)
        #         i_3 = list(set(i_1) & set(i_2))
        #         list_same = [i_3[0]]
        #         print("Совпадающие: ", i_3)
        #         print(type(list_same))
        #         print(list_same)
        #         context['intersection'] = i_3
        #         i_4 = context['intersection']
        #         print(i_4)
            differences = []
            res_diseases = []
            for disease in diseases:
                disease_ingr = disease.list_ingredient.all()
                print("disease_ingr:", disease_ingr)
                for recipe in recipes:
                    recipe_ingr = recipe.list_ingredient.all()
                    print("recipe_ingr:", recipe_ingr)
                    same = list(set(disease_ingr) & set(recipe_ingr))
                    print(same)
                # if
                    differences.append(same)
                # print(differences)
                    for i in differences:
                        print("diff ", i)

                #         res_diseases.append(disease)
                # print(res_diseases)

            result = list(filter(None, differences))
            print(result)
        # for i in differences:
        #     print(i)
            context['same'] = result
        # context['r_ingredients'] = i_1
        # context['d_ingredients'] = i_2

        return context

    #
    # def get_queryset(self):
    #     results = Recipe.objects.all()
    #     for staff in results:
    #         print(staff.list_ingredient.all())
    #         return staff


# class RecipeDetailView(DetailView):
#     model = Recipe
#     context_object_name = 'recipe'
#     template_name = 'recipes/recipe/recipe_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category_id'] = self.kwargs.get('pk')
#         context['list_ingredient'] = self.kwargs.get('pk')
#         context['blacklist'] = BlackList.objects.filter(user=self.request.user)
#
#         # context['blacklist_disease'] = BlackList.disease.objects.filter(user=self.request.user)
#         # disease = models.ForeignKey(Disease, related_name='blacklist_disease', blank=True, null=True, default=None,
#         #                             on_delete=models.CASCADE)
#
#         # context['list_ingredient'] = self.kwargs.get('pk')
#         return context

    # def get_queryset(self):
    #     recipe = Recipe.objects.filter(category_id=self.kwargs.get('pk'))
    #     # disease = get_object_or_404(Disease, id=id)
    #
    #     # recipe_ingr = Recipe.objects.filter(list_ingredient__name__icontains=self.request.recipe)
    #     # sitesubnet = Subnets.objects.filter(sitesubnets__site_id=site_id)
    #     # common_subnets = list(set(devicesubnet) & set(sitesubnet))
    #     return recipe


    # blacklist = BlackList.objects.filter(user=request.user)
    # def get_queryset(self):
    #     return self.model.objects.filter(friend_of=self.request.user.profile)


class SearchResultsListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        result = super(SearchResultsListView, self).get_queryset()
        q = self.request.GET.get('q')
        q = q.split(",")
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
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return super(CreateRecipeView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class SuccessDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe/recipe_created.html'

#
# def dispatch_by_user(RecipeDetailView, RecipeDetailNotLoggedView):
#     def get_view(request, **kwargs):
#         if is_logged_in__user(request.user):
#             return RecipeDetailView(request, **kwargs)
#         else:
#             return RecipeDetailNotLoggedView(request, **kwargs)
#
#
# def is_logged_in__user(user):
#     return user.is_active
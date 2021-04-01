from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify

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
        context['blacklist'] = BlackList.objects.filter(user=self.request.user)
        # context['blacklist_disease'] = BlackList.disease.objects.filter(user=self.request.user)
        # disease = models.ForeignKey(Disease, related_name='blacklist_disease', blank=True, null=True, default=None,
        #                             on_delete=models.CASCADE)

        # context['list_ingredient'] = self.kwargs.get('pk')
        return context

    # def get_queryset(self):
    #     return Recipe.objects.filter(category_id=self.kwargs.get('pk'))
    #

    # blacklist = BlackList.objects.filter(user=request.user)
    # def get_queryset(self):
    #     return self.model.objects.filter(friend_of=self.request.user.profile)
    #


class SearchResultsListView(ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'recipes/recipe/search_results.html'

    def get_queryset(self):
        queryset = super(SearchResultsListView, self).get_queryset()
        # q = self.request.GET.get('q')
        q = self.request.GET.get('q')
        q = q.split(",")
        # if not q:
        #     return []
        query = Q(list_ingredient__name=q[0]) | Q(list_ingredient__name=q[1])
        return Recipe.objects.filter(query)
            # .distinct()

        # q_lst = q.split(",")
        # return queryset.filter(
        #     # Q(name__icontains=query)
        #     Q(list_ingredient__name__in=q_lst[0]) | Q(list_ingredient__name__in=q_lst[1])
        #     # & Q(list_ingredient__name=q_lst[1])
        #     # Q(list_ingredient__name__in=keywords)
        #     # SearchQuery(query)
        # ).filter(status='p')

        # (Q(name__startswith="John") | Q(name__startswith="Paul")
        # Model.object.filter(Q(color=color[0]) & & Q(color=color[1]))
            # .annotate(rank=search_rank).order_by('-rank').values_list('name', 'rank')

# id_list = self.request.GET.getlist("id")
#         if not id_list:
#             return []
#         return Boat.objects.filter(id__in=id_list)

# class SearchResultsListView(ListView):
#     model = Recipe
#     context_object_name = 'recipe_list'
#     template_name = 'recipes/recipe/search_results.html'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         keywords = Ingredient.objects.values('name')
#         return Recipe.objects.filter(
#             # Q(name__icontains=query)
#             Q(list_ingredient__contains=query)
#             # Q(list_ingredient__name__in=keywords)
#             # SearchQuery(query)
#         ).filter(status='p')
#             # .values_list(keywords)





    # (Q(member=p1) | Q(member=p2))
    # .filter(status='p')
    # pk__in = [1, 4, 7]
# followers = UserFollowing.objects.filter(...).values('user')
# plants = Plant.objects.filter(owner__in = followers)

# current_user = request.user
# keywords=  ['funny', 'old', 'black_humor']
# qs = [Q(title__icontains=keyword)|Q(author__icontains=keyword)|Q(tags__icontains=keyword) for keyword in keywords]
#
# query = qs.pop() #get the first element
#
# for q in qs:
#     query |= q
# filtered_user_meme = Meme.objects.filter(query, user=current_user)

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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, RedirectView

from recipes.models import Recipe

from .models import *
from .forms import *


# class CartCreate(CreateView):
#     model = Cart
#     fields = '__all__'
#
#     # def form_valid(self, form):
#     #     form.instance.user = self.request.user
#     #     return super().form_valid(form)
#
#     def form_valid(self, form):
#         # cart = form.save(commit=False)
#         Cart.user = self.request.user
#         recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe'])
#         form.instance.recipe = recipe
#         # article.save()  # This is redundant, see comments.
#         return super(CartCreate, self).form_valid(form)


def cart(request):
    carts = Cart.objects.all()

    form = CartForm()

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/cart')
    context = {'carts': carts, 'cart_form': form}
    return render(request, 'cart/index.html', context)


@login_required
def cart_view(request, id):
    cart = get_object_or_404(Cart, id=id)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart.user = request.user
            cart.save()
            return redirect('/')
    else:
        form = CartForm()
    # return render(request, 'recipes/recipe/recipe_detail.html', {'cart_form': form})
    return render(request, 'cart/index.html', {'cart_form': form, 'cart': cart})


# class CartCreate(CreateView):
#     model = Cart
#     fields = '__all__'
#     template_name = 'cart/index.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super(CartCreate, self).form_valid(form)


class CartCreate(LoginRequiredMixin, CreateView):
    model = Cart
    fields = '__all__'

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)
    #
    # def get(self, request, *args, **kwargs):
    #     Cart(user=request.user).save()
    #     return HttpResponseRedirect('/')


def index(request):
    tasks = Task.objects.all()

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/cart')
    context = {'tasks': tasks, 'form': form}
    return render(request, 'cart/list.html', context)


def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/cart')

    context = {'form': form}
    return render(request, 'cart/update_task.html', context)


def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/cart')

    context = {'item': item}
    return render(request, 'cart/delete.html', context)


# @login_required
# def cart_list(request):
#     cart = Recipe.objects.filter(cart=request.user)
#     return render(request,
#                   'account/cart.html',
#                   {'cart': cart})
#
#
# @login_required
# def add_to_cart(request, id):
#     recipe = get_object_or_404(Recipe, id=id)
#     if recipe.cart.filter(id=request.user.id).only('name', 'list_ingredient').exists():
#         recipe.cart.remove(request.user)
#     else:
#         recipe.cart.add(request.user).only('name', 'list_ingredient')
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


# class CartDetail(DetailView):
#     model = Cart
#     template_name = 'Cart'
#
#
# class CartList(ListView):
#     model = Cart
#     context_object_name = 'cart'
#     template_name = 'cart/cart_list.html'
#
#
# class CreateCart(CreateView):
#     model = Cart
#     template_name = 'cart/cart_create.html'


@login_required
def cart_list(request):
    cart = Recipe.objects.filter(cart=request.user)
    return render(request,
                  'cart/cart.html',
                  {'cart': cart})


@login_required
def add_to_cart(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.cart.filter(id=request.user.id).exists():
        recipe.cart.remove(request.user)
    else:
        recipe.cart.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# @login_required
# def add_to_cart(request, id):
#     cart = get_object_or_404(Cart, id=id)
#     if cart.user == request.user.id:
#         recipe.cart.remove(request.user)
#     else:
#         recipe.cart.add(request.user)
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


# class CreateCartView(CreateView):
#     model = Cart
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(CreateCartView, self).form_valid(form)


#
# class CreateRecipeView(CreateView):
#     model = Recipe
#     form_class = RecipeCreateForm
#     template_name = 'recipes/recipe/recipe_create.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(CreateRecipeView, self).form_valid(form)

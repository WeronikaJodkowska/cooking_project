from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from recipes.models import Recipe

from .models import *
from .forms import *


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

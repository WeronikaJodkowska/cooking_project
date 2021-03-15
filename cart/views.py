from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

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


@login_required
def cart_list(request):
    # cart = Cart.objects.all().filter(user=request.user)
    cart = Cart.objects.filter(user=request.user)
    return render(request,
                  'cart/cart.html',
                  {'cart': cart})


@login_required
def add_to_cart(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user = get_object_or_404(User, id=request.user.id)
    # if Cart.objects.all().filter(id=request.user.id).exists():
    #     cart = Cart(recipe=recipe, user=user)
    #     cart.delete()
    # else:
    if not Cart.objects.all().filter(recipe=recipe).exists():
        cart = Cart(recipe=recipe, user=user)
        cart.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def delete_from_cart(request, id):
    Cart.objects.filter(id=id).delete()
    return HttpResponseRedirect('/cart/cart')

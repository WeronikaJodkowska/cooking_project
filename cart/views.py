from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, RedirectView

from recipes.models import Recipe

from .models import *
from .forms import *


class CreateCart(CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'cart/cart.html'

    # def get_success_url(self):
    #     return reverse('recipes:recipe_detail', args=[self.recipe.id])

    # def get_context_data(self, **kwargs):
    #     self.recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
    #     kwargs['recipe'] = self.recipe
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        """ Exclude any unpublished questions. """
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        return recipe

    # def form_valid(self, form):
    #     # self.recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
    #     # form.instance.recipe = self.recipe
    #     return super().form_valid(form)
    # def get_context_data(self, **kwargs):
    #     self.recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
    #     kwargs['recipe'] = self.recipe
    #     return super().get_context_data(**kwargs)
    # def form_valid(self, form):
    #     self.recipe = get_object_or_404(Recipe, id=self.kwargs['recipe_id'])
    #     form.instance.recipe = self.recipe
    #     return super().form_valid(form)

    def form_valid(self, form):
        cart_obj = form.save(commit=False)
        cart_obj.user = self.request.user
        recipe = get_object_or_404(Recipe, slug=self.kwargs['pk'])
        form.instance.recipe = recipe
        cart_obj.save()
        # return super(CreateCart, self).form_valid(form)

        return HttpResponseRedirect(reverse('recipes:recipe_list'))


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
    cart = Recipe.objects.filter(cart=request.user)
    return render(request,
                  'cart/cart.html',
                  {'cart': cart})


@login_required
def add_to_cart(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    user = get_object_or_404(User, id=request.user.id)
    cart = Cart(recipe=recipe, user=user)  # Case of update
    cart.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




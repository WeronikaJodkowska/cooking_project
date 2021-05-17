from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify
from django.views.generic.edit import FormMixin, SingleObjectMixin
from django.views import View

from .models import DiseaseCategory, Disease, BlackList
# from .forms import BlackListCreateForm


class CategoryListView(ListView):
    model = DiseaseCategory
    context_object_name = 'category_list'
    template_name = 'diseases/categories/category_list.html'


class CategoryDetailView(DetailView):
    model = DiseaseCategory
    context_object_name = 'category'
    template_name = 'diseases/categories/category_detail.html'


class DiseaseListView(ListView):
    model = Disease
    template_name = 'diseases/disease/disease_list.html'

    # def get_queryset(self):
    #     return Disease.objects.filter(status='p')


class DiseaseDetailView(DetailView):
    model = Disease
    context_object_name = 'disease'
    # form_class = BlackListCreateForm
    template_name = 'diseases/disease/disease_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('pk')
        # context['form'] = BlackListCreateForm(initial={'self_ingredients': self.object})
        return context

    #
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    #     form.save()
    #     return super(DiseaseDetailView, self).form_valid(form)


class PostBlacklist(SingleObjectMixin, View):
    model = BlackList
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #
    #     return render(request, '')

    def post(self, request, *args, **kwargs):
        self.object =self.get_object()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_to_blacklist(request, id):
    disease = get_object_or_404(Disease, id=id)
    user = get_object_or_404(User, id=request.user.id)
    success_message = 'Disease added to the blacklist.'

    if not BlackList.objects.all().filter(disease=disease).exists():
        blacklist = BlackList(user=user, disease=disease)
        blacklist.save()
        # messages.success(request, "Successfully added")
    # else:
        # messages.error(request, 'Already exists')
    # cart.disease.add(disease)
    # self_ingredients = super(DiseaseDetailView, self).get_context_data(**kwargs)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class CreateBlacklist(LoginRequiredMixin, CreateView, SingleObjectMixin):
    model = BlackList
    # form_class = BlackListCreateForm
    template_name = 'diseases/disease/disease_detail.html'
    success_url = "/diseases"
    #
    # def post(self, request, *args, **kwargs):
    #     # form.instance.user = self.request.user
    #     # disease = get_object_or_404(Disease, id=id)
    #     self.object = self.get_object()
    #     blacklist = BlackList(user=self.request.user)
    #     blacklist.save()
    #     blacklist.disease.add(self.object.disease)
    #     # form.save()
    #     return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def form_valid(self, form):
        form.save()
        return super(CreateBlacklist, self).form_valid(form)


@login_required
def black_list(request):
    blacklist = BlackList.objects.filter(user=request.user)
    return render(request,
                  'diseases/blacklist/blacklist.html',
                  {'blacklist': blacklist})


@login_required
def delete_from_blacklist(request, id):
    BlackList.objects.filter(id=id).delete()
    return HttpResponseRedirect('/diseases/blacklist')

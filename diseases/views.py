from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import SingleObjectMixin
from django.views import View

from .models import DiseaseCategory, Disease, BlackList


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


class DiseaseDetailView(DetailView):
    model = Disease
    context_object_name = 'disease'
    template_name = 'diseases/disease/disease_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        disease = get_object_or_404(Disease, id=self.kwargs['pk'])
        blacklisted = False
        if BlackList.objects.filter(user=self.request.user.id, disease=disease).exists():
            blacklisted = True
        context['disease_is_blacklisted'] = blacklisted

        context['category_id'] = self.kwargs.get('pk')
        return context


class PostBlacklist(SingleObjectMixin, View):
    model = BlackList

    def post(self, request, *args, **kwargs):
        self.object =self.get_object()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_to_blacklist(request, id):
    disease = get_object_or_404(Disease, id=id)
    user = get_object_or_404(User, id=request.user.id)
    success_message = 'Disease added to the blacklist.'

    if BlackList.objects.all().filter(disease=disease).filter(user=request.user.id).exists():
        print("deleted")
        blacklist = BlackList.objects.get(user=user, disease=disease)
        blacklist.delete()
    else:
        print("created")
        blacklist = BlackList(user=user, disease=disease)
        blacklist.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class CreateBlacklist(LoginRequiredMixin, CreateView, SingleObjectMixin):
    model = BlackList
    template_name = 'diseases/disease/disease_detail.html'
    success_url = "/diseases"

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

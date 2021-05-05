import os
from dal import autocomplete
from django import forms
from django.forms import ImageField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from ingredients.models import Ingredient
from .models import Recipe, Category


class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'recipes/recipe/checkbox_option.html'
    queryset = Category.objects.all()


class RecipeCreateForm(autocomplete.FutureModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control form-control-sm"}))
    preparation_time = forms.CharField(label='Cook time',
                                       widget=forms.TextInput(attrs={"class": "form-control form-control-sm",
                                                                     'placeholder': '1 hr 30 mins'}))
    image = forms.ImageField(error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput)
    direction = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))

    class Meta:
        model = Recipe
        fields = ('name', 'category', 'image',)
        # widgets = {
        #     'list_ingredient': autocomplete.ModelSelect2Multiple(url='recipes:ingredient_autocomplete')
        # }

    # category = models.ForeignKey(Category, related_name='recipes', on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, db_index=True)
    # slug = models.SlugField(max_length=200, db_index=True)
    # directions = models.TextField(default=None)
    # image = models.ImageField(upload_to='recipes/%Y/%m/%d')
    # favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    # list_ingredient = models.ManyToManyField(Ingredient)
    # # users = models.ManyToManyField('auth.User', null=True, blank=True)
    # cart = models.ManyToManyField(User, related_name='cart', default=None, blank=True)


    @property
    def image_name(self):
        return os.path.basename(self.image.path) if self.image else ''
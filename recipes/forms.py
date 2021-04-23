import os
from dal import autocomplete
from django import forms
from django.forms import ImageField

from ingredients.models import Ingredient
from .models import Recipe, Category


class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'recipes/recipe/checkbox_option.html'
    queryset = Category.objects.all()


class RecipeCreateForm(autocomplete.FutureModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control form-control-sm"}))
    # , widget=MyCheckboxSelectMultiple)
    # list_ingredient = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
    #                                                  widget=forms.CheckboxSelectMultiple)
    # list_ingredient = autocomplete.QuerySetSequenceSelect2Multiple(
    #     queryset=Ingredient.objects.all(),
    #     required=False,
    #     widget=autocomplete.QuerySetSequenceSelect2Multiple(
    #         'recipes:ingredient_autocomplete'),
    # )

    image = forms.ImageField(error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput)
    # (attrs={"class": "form-control form-control-sm"}))
    directions = forms.Textarea()

    # list_ingredient = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
    #                                                  widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Recipe
        fields = ('name', 'category', 'list_ingredient', 'image', 'directions',)
        widgets = {
            'list_ingredient': autocomplete.ModelSelect2Multiple(url='recipes:ingredient_autocomplete')
        }
        # list_ingredient = forms.MultipleChoiceField(required=False)

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
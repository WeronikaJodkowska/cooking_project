import os
from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import ImageField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django_select2.forms import Select2MultipleWidget
from easy_select2 import Select2
from searchableselect.widgets import MultiValueDict

from .custom_layout_object import *

from ingredients.models import Ingredient
from .models import *


class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'recipes/recipe/checkbox_option.html'
    queryset = RecipeCategory.objects.all()


class RecipeCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
    # category = forms.ModelChoiceField(queryset=RecipeCategory.objects.all(),
    #                                   widget=autocomplete.ModelSelect2(url='recipes:category-autocomplete'))
    #                                                                    # attrs={"class": "form-control form-control-sm"}))
    category = forms.ModelChoiceField(queryset=RecipeCategory.objects.all(), widget=Select2(attrs={"class": "form-control form-control-sm"}))
    # widget=autocomplete.ModelSelect2(url='recipes:category_autocomplete'))
    preparation_time = forms.CharField(label='Cook time',
                                       widget=forms.TextInput(attrs={"class": "form-control form-control-sm",
                                                                     'placeholder': '1 hr 30 mins'}))
    image = forms.ImageField(error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput(attrs={"class": "form-control form-control-sm"}))

    # queryset = (Category.objects.all())
    # category = forms.MultipleChoiceField(choices=queryset, widget=Select2MultipleWidget)

    # direction = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['slug', 'favourites', 'status', 'user']
        # fields = ('name', 'category', 'image',)
        # widgets = {
        #     'category': autocomplete.ModelSelect2(url='recipes:category-autocomplete',
        #                                                  attrs={"class": "form-control form-control-sm"})
        # }

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.fields["category"].label = "Category"

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('category'),
                Field('preparation_time'),
                Field('image'),
                HTML("<br>"),
                Fieldset('Add ingredients',
                         Formset('ingredients')),
                HTML("<br>"),
                Fieldset('Add directions',
                         Formset('directions')),
                # HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

    @property
    def image_name(self):
        return os.path.basename(self.image.path) if self.image else ''

    # @property
    # def helper(self):
    #     helper = FormHelper()
    #     helper.form_tag = False
    #     helper.layout = Layout(Fieldset('Create new recipe'), )
    #     return helper


# class DirectionFormHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super(DirectionFormHelper, self).__init__(*args, **kwargs)
#         self.form_tag = False
#         self.layout = Layout(Fieldset("Add recipe direction"), )


class RecipeDirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['text', 'image']

    @property
    def image_name(self):
        return os.path.basename(self.image.path) if self.image else ''


class TextArea(object):
    pass


class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        exclude = ()


RecipeDirectionFormSet = inlineformset_factory(
    Recipe,
    Direction,
    form=RecipeDirectionForm,
    fields=('text', 'image',),
    extra=3,
    can_delete=True,
    widgets={
        'text': forms.TextInput(attrs={"class": "form-control form-control-sm"}),
        'image': forms.FileInput(attrs={"class": "form-control form-control-sm"}),
    }
)

RecipeIngredientsFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredients,
    form=RecipeIngredientsForm,
    fields='__all__',
    extra=3,
    can_delete=True,
    widgets={
        'amount': forms.TextInput(attrs={"class": "form-control form-control-sm"}),
        'unit': forms.Select(attrs={"class": "form-control form-control-sm"}),
        'ingredient': forms.Select(attrs={"class": "form-control form-control-sm"}),
    }
)

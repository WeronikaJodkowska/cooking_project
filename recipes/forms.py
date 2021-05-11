import os
from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import ImageField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *

from ingredients.models import Ingredient
from .models import *


class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'recipes/recipe/checkbox_option.html'
    queryset = Category.objects.all()


class RecipeCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control form-control-sm"}))
    preparation_time = forms.CharField(label='Cook time',
                                       widget=forms.TextInput(attrs={"class": "form-control form-control-sm",
                                                                     'placeholder': '1 hr 30 mins'}))
    image = forms.ImageField(error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput)

    # direction = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))

    class Meta:
        model = Recipe
        exclude = ['slug', 'favourites', 'status', 'user']
        # fields = ('name', 'category', 'image',)
        # widgets = {
        #     'list_ingredient': autocomplete.ModelSelect2Multiple(url='recipes:ingredient_autocomplete')
        # }

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
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
                Fieldset('Add directions',
                         Formset('directions')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

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
        exclude = ()


class TextArea(object):
    pass


RecipeDirectionFormSet = inlineformset_factory(
    Recipe,
    Direction,
    form=RecipeDirectionForm,
    fields=('text', 'image',),
    extra=3,
    can_delete=False,
    widgets={
        'text': forms.TextInput(attrs={"class": "form-control form-control-sm"})
    }
)

from django import forms

from .models import Recipe


class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('name', 'category', 'image', 'directions', 'list_ingredient',)
        list_ingredient = forms.MultipleChoiceField(required=False)


    # category = models.ForeignKey(Category, related_name='recipes', on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, db_index=True)
    # slug = models.SlugField(max_length=200, db_index=True)
    # directions = models.TextField(default=None)
    # image = models.ImageField(upload_to='recipes/%Y/%m/%d')
    # favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    # list_ingredient = models.ManyToManyField(Ingredient)
    # # users = models.ManyToManyField('auth.User', null=True, blank=True)
    # cart = models.ManyToManyField(User, related_name='cart', default=None, blank=True)

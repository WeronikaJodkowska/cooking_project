from django import forms

from .models import BlackList


class BlackListCreateForm(forms.ModelForm):

    class Meta:
        model = BlackList
        # fields = ('self_ingredients',)
        # self_ingredients = forms.MultipleChoiceField(required=False)
    #
    # user = models.ForeignKey(User, blank=True, related_name='blacklist_user',
    #                          null=True, default=None, on_delete=models.CASCADE)
    # disease = models.ManyToManyField(Disease, related_name='blacklist_disease', blank=True, default=None)
    # self_ingredients = models.ManyToManyField(Ingredient, related_name='blacklist_ingredients', blank=True, default=None)
    #
    # def __str__(self):
    #     return str(self.id)

    # def get_ingredients_by_disease(self, obj):
    #     return "\n".join([p.list_ingredient for p in obj.Disease.all()])


from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from ingredients.models import Ingredient


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='disease_categories/%Y/%m/%d')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diseases:category_list', args=[self.slug])


class Disease(models.Model):
    category = models.ForeignKey(Category, related_name='diseases', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    # favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    list_ingredient = models.ManyToManyField(Ingredient, related_name='disease_ingredients', blank=True, default=None)
    # ingredients = models.ForeignKey(Ingredient, related_name='disease_ingredients',
    #                                 null=True, blank=True, default=None,
    #                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('recipes:recipe_detail',
    #                    args=[self.id, self.slug])
    #
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Recipe, self).save(*args, **kwargs)


class BlackList(models.Model):
    user = models.ForeignKey(User, blank=True, related_name='blacklist_user',
                             null=True, default=None, on_delete=models.CASCADE)
    disease = models.ManyToManyField(Disease, related_name='blacklist_disease', blank=True, default=None)
    self_ingredients = models.ManyToManyField(Ingredient, related_name='blacklist_ingredients', blank=True, default=None)

    def __str__(self):
        return str(self.id)

    # def get_ingredients_by_disease(self, obj):
    #     return "\n".join([p.list_ingredient for p in obj.Disease.all()])



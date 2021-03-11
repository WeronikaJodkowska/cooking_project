from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from ingredients.models import Ingredient


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:recipe_list_by_category', args=[self.slug])


class Recipe(models.Model):
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    ]

    category = models.ForeignKey(Category,
                                 related_name='recipes',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    directions = models.TextField(default=None)
    image = models.ImageField(upload_to='recipes/%Y/%m/%d')
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    list_ingredient = models.ManyToManyField(Ingredient, blank=True)
    # users = models.ManyToManyField('auth.User', null=True, blank=True)
    cart = models.ManyToManyField(User, related_name='cart', default=None, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail',
                       args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

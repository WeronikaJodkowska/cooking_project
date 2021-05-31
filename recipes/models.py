from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from positions.fields import PositionField
from ingredients.models import Ingredient


class RecipeCategory(models.Model):
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
    category = models.ForeignKey(RecipeCategory,
                                 related_name='recipes',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    preparation_time = models.CharField(max_length=10, blank=True,
                                        help_text="Enter time in minutes or hours",
                                        verbose_name='preparation time')
    image = models.ImageField(upload_to='recipes/%Y/%m/%d')
    favourites = models.ManyToManyField(User, related_name='favourite',
                                        default=None, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    user = models.ForeignKey(User, blank=True, null=True, default=None,
                             on_delete=models.CASCADE)

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


class Direction(models.Model):
    order = PositionField(blank=True, null=True, unique_for_field='recipe')
    text = models.TextField(blank=True, verbose_name='direction|text')
    image = models.ImageField(blank=True, upload_to='directions/%Y/%m/%d')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Direction'
        verbose_name_plural = 'Directions'
        ordering = ['order', 'id']


class MeasurementUnits(models.Model):
    name = models.CharField(max_length=20, verbose_name='Measurement Unit')
    long_name = models.CharField(max_length=20, blank=True,
                                 verbose_name='long name')

    class Meta:
        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               blank=True, default=None)
    amount = models.FloatField(max_length=100, blank=True,
                               null=True, default=None)
    unit = models.ForeignKey(MeasurementUnits, on_delete=models.CASCADE,
                             blank=True, null=True, default=None)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   blank=True, default=None)

    class Meta:
        verbose_name = 'Recipe Ingredients'
        verbose_name_plural = 'Recipe Ingredients'

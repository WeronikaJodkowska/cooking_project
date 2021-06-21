from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ingredients.models import Ingredient


class DiseaseCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, default=None,
                              upload_to='disease_categories/%Y/%m/%d')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(DiseaseCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('diseases:category_list', args=[self.slug])


class Disease(models.Model):
    category = models.ForeignKey(DiseaseCategory,
                                 related_name='diseases',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    list_ingredient = models.ManyToManyField(Ingredient,
                                             related_name='disease_ingredients',
                                             blank=True, default=None)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Disease, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('diseases:disease_detail', args=[self.slug])


class BlackList(models.Model):
    user = models.ForeignKey(User, blank=True,
                             related_name='blacklist_user',
                             null=True, default=None,
                             on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,
                                related_name='blacklist_disease',
                                blank=True, null=True, default=None,
                                on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

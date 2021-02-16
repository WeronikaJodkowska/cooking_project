from django.db import models


# class Teacher(models.Model):
#     name = models.CharField(max_length=80)
#     age = models.IntegerField()
#     new_field = models.CharField(max_length=140, default='SOME STRING')


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',),
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    # category
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='ingredients/%Y/%m/%d')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

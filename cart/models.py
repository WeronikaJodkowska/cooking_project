from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from recipes.models import Recipe


class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class Cart(models.Model):
#     # recipe_name = models.ForeignKey(Recipe.name, related_name='recipe_name', blank=True, default=None,
#     #                                 on_delete=models.CASCADE)
#     # recipe_ingredients = models.ForeignKey(Recipe.list_ingredient, blank=True, default=None,
#     #                                        on_delete=models.CASCADE)
#     recipe = models.ManyToManyField(Recipe, null=True, blank=True)
#     user = models.ForeignKey(User, blank=True, default=None, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=datetime.now)

#
# class CartItem(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.recipe

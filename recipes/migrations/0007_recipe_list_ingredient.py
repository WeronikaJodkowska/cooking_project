# Generated by Django 3.1.6 on 2021-02-26 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0006_ingredient_favourites'),
        ('recipes', '0006_recipe_favourites'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='list_ingredient',
            field=models.ManyToManyField(to='ingredients.Ingredient'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-03-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0006_ingredient_favourites'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='list_ingredient',
        ),
        migrations.AddField(
            model_name='recipe',
            name='list_ingredient',
            field=models.ManyToManyField(blank=True, to='ingredients.Ingredient'),
        ),
    ]

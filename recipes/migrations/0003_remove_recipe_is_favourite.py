# Generated by Django 3.1.6 on 2021-02-18 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipe_is_favourite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='is_favourite',
        ),
    ]
# Generated by Django 3.1.6 on 2021-03-01 06:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_recipe_list_ingredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cart',
            field=models.ManyToManyField(blank=True, default=None, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
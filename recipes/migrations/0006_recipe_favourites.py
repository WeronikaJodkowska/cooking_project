# Generated by Django 3.1.6 on 2021-02-24 11:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_auto_20210222_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favourites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.1.6 on 2021-05-14 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0006_ingredient_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='favourites',
        ),
    ]

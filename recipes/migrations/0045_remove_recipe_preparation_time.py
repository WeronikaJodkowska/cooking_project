# Generated by Django 3.1.6 on 2021-06-22 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0044_auto_20210516_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='preparation_time',
        ),
    ]

# Generated by Django 3.1.6 on 2021-06-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0046_recipe_the_timedelta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='the_timedelta',
        ),
        migrations.AddField(
            model_name='recipe',
            name='preparation_time',
            field=models.DurationField(blank=True, null=True, verbose_name='Preparation time'),
        ),
    ]
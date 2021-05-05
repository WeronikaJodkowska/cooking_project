# Generated by Django 3.1.6 on 2021-05-05 13:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0027_auto_20210505_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.TextField(blank=True, help_text='Enter time in minutes or hours', max_length=10, validators=[django.core.validators.RegexValidator(regex='[0-100] min')], verbose_name='preparation time'),
        ),
    ]

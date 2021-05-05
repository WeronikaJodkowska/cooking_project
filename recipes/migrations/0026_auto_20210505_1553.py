# Generated by Django 3.1.6 on 2021-05-05 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0025_auto_20210505_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.TextField(blank=True, help_text='Enter time in minutes or hours', max_length=10, verbose_name='preparation time'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-04-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20210428_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='preparation_time',
            field=models.TextField(blank=True, help_text='Enter time in minutes or hours', verbose_name='preparation time'),
        ),
    ]
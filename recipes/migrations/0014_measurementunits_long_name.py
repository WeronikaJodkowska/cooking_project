# Generated by Django 3.1.6 on 2021-04-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20210428_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurementunits',
            name='long_name',
            field=models.TextField(blank=True, verbose_name='long name'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-05-16 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0043_auto_20210516_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurementunits',
            name='long_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='long name'),
        ),
        migrations.AlterField(
            model_name='measurementunits',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Measurement Unit'),
        ),
    ]
# Generated by Django 3.1.6 on 2021-04-28 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_measurementunits_long_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurementunits',
            name='name',
            field=models.TextField(verbose_name='Measurement Unit'),
        ),
    ]

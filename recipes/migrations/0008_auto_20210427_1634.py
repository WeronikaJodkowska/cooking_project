# Generated by Django 3.1.6 on 2021-04-27 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_direction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='image',
            field=models.ImageField(blank=True, upload_to='directions/%Y/%m/%d'),
        ),
    ]

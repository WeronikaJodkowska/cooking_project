# Generated by Django 3.1.6 on 2021-04-27 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210427_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='directions',
        ),
        migrations.DeleteModel(
            name='Direction',
        ),
    ]

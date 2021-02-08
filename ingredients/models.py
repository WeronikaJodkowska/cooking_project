from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()
    new_field = models.CharField(max_length=140, default='SOME STRING')
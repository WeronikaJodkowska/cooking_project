# from django.contrib.auth.models import User
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(
#         upload_to='assets/images',
#         default='no-img.jpg',
#         blank=True
#     )
#     first_name = models.CharField(max_length=255, default='')
#     last_name = models.CharField(max_length=255, default='')
#     email = models.EmailField(default='none@email.com')
#     birth_date = models.DateField(default='1999-12-31')
#
#     def __str__(self):
#         return self.user.username
#
#
# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         profile = Profile.objects.create(user=kwargs['instance'])
#
#
# post_save.connect(create_profile, sender=User)

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=20, null=False)
    phone_number = models.CharField(max_length=20, null=False)
    birthday = models.CharField(max_length=10, null=False)
    gender = models.CharField(max_length=10, null=False)
    nation = models.CharField(max_length=30, null=False)
    profile_image = models.ImageField(null=True, upload_to='profiles/%Y/%m/%d')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Trip(models.Model):
    title = models.CharField(max_length=40, null=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    owner_index = models.IntegerField(null=False)


class Position(models.Model):
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)
    time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Article(models.Model):
    content = models.TextField(max_length=500, null=False)
    time = models.DateTimeField(auto_now_add=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class ImageInArticle(models.Model):
    image = models.ImageField(null=False, upload_to='uploads/%Y/%m/%d')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
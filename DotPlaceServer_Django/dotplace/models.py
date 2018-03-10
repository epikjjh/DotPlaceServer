import os
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from DotPlaceServer_Django import settings
from dotplace.process_image import create_thumbnail


class UserManager(BaseUserManager):
    def create_user(self, user_name, phone_number, email, password, birthday, gender, nation, profile_image,
                    **extra_fields):
        if not user_name:
            raise ValueError('User name required')
        if not phone_number:
            raise ValueError('Phone number required')
        if not email:
            raise ValueError('Email address required')
        if not birthday:
            raise ValueError('Birthday required')
        if not gender:
            raise ValueError('Gender required')
        if not nation:
            raise ValueError('Nation required')

        user = self.model(user_name=user_name, phone_number=phone_number, email=self.normalize_email(email),
                          birthday=birthday, gender=gender, nation=nation, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        code = '0'

        if profile_image:
            try:
                user.profile_image = profile_image
                user.save(using=self._db)
                create_thumbnail('user/profile_image_{profile_id}.jpeg'.format(profile_id=user.pk), (400, 300))
            except FileNotFoundError:
                code = ''
                user.delete()

        return user, code

    def create_super_user(self, user_name, phone_number, email, password, **extra_fields):
        user = self.model(user_name=user_name, phone_number=phone_number, email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)

        return user


def profile_image_path(instance, filename):
    return 'user/profile_image_{profile_id}.jpeg'.format(profile_id=instance.id)


class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=20)
    phone_number = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True, max_length=25)
    birthday = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    nation = models.CharField(max_length=30)
    profile_image = models.ImageField(null=True, upload_to=profile_image_path)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name', 'email', 'birthday', 'gender', 'nation', 'profile_image']

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.profile_image
            self.image = None
            super(User, self).save(*args, **kwargs)
            self.profile_image = saved_image
        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        try:
            code = '0'
            os.remove('user/profile_image_{user_id}.jpeg'.format(user_id=self.pk))
            os.remove('user/profile_image_{user_id}_thumbnail.jpeg'.format(user_id=self.pk))
        except FileNotFoundError:
            code = ''
        super(User, self).delete()

        return code

    def __str__(self):
        return '{id}'.format(id=self.user_name)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Trip(models.Model):
    title = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_index = models.IntegerField()


class Position(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField()
    duration = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Article(models.Model):
    content = models.TextField(max_length=500)
    time = models.DateTimeField(auto_now=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


def article_image_path(instance, filename):
    return 'article/article_image_{article_id}/{id}.jpeg'.format(article_id=instance.article.id, id=instance.id)


class ArticleImage(models.Model):
    image = models.ImageField(upload_to=article_image_path)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(ArticleImage, self).save(*args, **kwargs)
            self.image = saved_image

        super(ArticleImage, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        try:
            code = '0'
            os.remove('article/article_image_{article_id}/{article_image_id}.jpeg'
                      .format(article_id=self.article.pk, article_image_id=self.pk))
            os.remove('article/article_image_{article_id}/{article_image_id}_thumbnail.jpeg'
                      .format(article_id=self.article.pk, article_image_id=self.pk))
        except FileNotFoundError:
            code = ''

        super(ArticleImage, self).delete()

        return code


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    time = models.DateTimeField(auto_now=True)
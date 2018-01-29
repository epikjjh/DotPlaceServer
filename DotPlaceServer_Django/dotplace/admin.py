from django.contrib import admin
from dotplace.models import Position
from dotplace.models import Trip
from dotplace.models import Article
from dotplace.models import Profile
from dotplace.models import ImageInArticle


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthday', 'gender', 'nation', 'profile_image']
    list_display_links = ['user', 'profile_image']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['content', 'position', 'time']
    list_display_links = ['position']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'owner_index']
    list_display_links = ['owner']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['lat', 'lng', 'time', 'type', 'duration', 'trip']
    list_display_links = ['trip']


@admin.register(ImageInArticle)
class ImageInArticleAdmin(admin.ModelAdmin):
    list_display = ['image', 'article']
    list_display_links = ['image', 'article']

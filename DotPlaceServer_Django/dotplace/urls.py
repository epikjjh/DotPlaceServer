from django.urls import path
from dotplace import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('login', views.login),
    path('user/new', views.create_user, name='create user'),
    path('trip_position/new', views.create_trip_and_position, name='create trip and position'),
    path('article/new', views.create_article, name='create article'),
    path('user/view', views.show_user, name='user list'),
    path('trip/view', views.show_trip, name='trip list'),
    path('position/view', views.show_position, name='position list'),
    path('article/view', views.show_article, name='article list'),
    path('article/search/trip_id', views.search_article_by_trip_id),
    path('article/search/radius', views.search_article_by_radius),
]
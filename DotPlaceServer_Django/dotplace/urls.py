from django.urls import path
from dotplace import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('sign_in', views.sign_in),
    path('sign_up', views.sign_up, name='sign up'),
    path('trip/new', views.create_trip, name='create trip'),
    path('position/new', views.create_position, name='create position'),
    path('article/new', views.create_article, name='create article'),
    path('article_image/new', views.create_article_image, name='create article image'),
    path('user/view', views.show_user, name='user list'),
    path('trip/view', views.show_trip, name='trip list'),
    path('position/view', views.show_position, name='position list'),
    path('article/view', views.show_article, name='article list'),
    path('article/search/trip_id', views.search_article_by_trip_id),
    path('article/search/radius', views.search_article_by_radius),
]
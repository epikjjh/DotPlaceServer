from django.urls import path
from dotplace import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('sign_in', views.sign_in),
    path('sign_up', views.sign_up),
    path('sign_out', views.sign_out),
    path('trip/new', views.create_trip),
    path('position/new', views.create_position),
    path('article/new', views.create_article),
    path('article_image/new', views.create_article_image),
    path('user/view', views.show_user, name='user list'),
    path('trip/view', views.show_trip, name='trip list'),
    path('position/view', views.show_position, name='position list'),
    path('article/view', views.show_article, name='article list'),
    path('news_feed/view', views.news_feed),
    path('article/search/trip_id', views.search_article_by_trip_id),
    path('article/search/radius', views.search_article_by_radius),
    path('article/search/id', views.search_article_by_id),
    path('user/search/id', views.search_user_by_id),
    path('image/search/id', views.return_file),
]
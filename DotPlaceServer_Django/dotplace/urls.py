from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from dotplace import views

urlpatterns = [
    path('sign_in', obtain_auth_token),
    path('sign_up', views.sign_up),
    path('sign_out', views.sign_out),
    path('change_pw', views.change_pw),
    path('change_info', views.change_info),
    path('withdrawal', views.withdrawal),
    path('user/search', views.search_user_by_id),
    path('trip/new', views.create_trip),
    path('position/new', views.create_position),
    path('article/new', views.create_article),
    path('article_image/new', views.create_article_image),
    path('article/search/trip_id', views.search_article_by_trip_id),
    path('article/search/radius', views.search_article_by_radius),
    path('article/search/id', views.search_article_by_id),
    path('news_feed/view', views.news_feed),
    path('image/search/id', views.return_file),
    path('comment/new', views.create_comment),
    path('comment/search/article_id', views.search_comment_by_article_id),
]
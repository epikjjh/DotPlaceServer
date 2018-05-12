from django.urls import path
from dotplace import views


urlpatterns = [
    path('user', views.UserView.as_view()),
    path('sign_up', views.sign_up),
    path('sign_in', views.SignIn.as_view()),
    path('sign_out', views.sign_out),
    path('change_pw', views.change_pw),
    path('article', views.ArticleView.as_view()),
    path('article/search/radius', views.search_article_by_radius),
    path('article/search/trip_id', views.search_article_by_trip_id),
    path('news_feed', views.news_feed),
    path('comment', views.CommentView.as_view()),
    path('comment/search/article_id', views.search_comment_by_article_id),
    path('trip', views.TripView.as_view()),
    path('position', views.PositionView.as_view()),
    path('article_image', views.ArticleImageView.as_view()),
    path('profile_image', views.ProfileImageView),
    path('profile_image_thumbnail', views.return_profile_image_thumbnail),
    path('article_image_thumbnail', views.return_article_image_thumbnail),
    path('follow', views.FollowView.as_view()),
]
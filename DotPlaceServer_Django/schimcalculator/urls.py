from django.urls import path
from schimcalculator import views

urlpatterns = [
    path('dotplace', views.DotPlaceView.as_view()),
]
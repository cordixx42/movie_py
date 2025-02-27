# homepage/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movieId>/', views.movie_detail, name='movie_detail'),
]

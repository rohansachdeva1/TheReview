from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('view_playlist/<int:playlist_id>/', views.view_playlist, name="view_playlist"),
    path('add_to_playlist/<int:entity_id>/', views.add_to_playlist, name="add_to_playlist"),
    path('add_to_new_playlist/<int:entity_id>/', views.add_to_new_playlist, name="add_to_new_playlist"),
    path('add_to_watchlater/<int:entity_id>/', views.add_to_watchlater, name="add_to_watchlater"),
    path('delete_from_playlist/<int:entity_id>/<int:playlist_id>/', views.delete_from_playlist, name="delete_from_playlist"),
    path('delete_from_watchlater/<int:entity_id>/', views.delete_from_watchlater, name="delete_from_watchlater"),
    path('delete_playlist/<int:playlist_id>/', views.delete_playlist, name="delete_playlist"),
    path('like_playlist/<int:playlist_id>/', views.like_playlist, name="like_playlist"),
    path('comment_playlist/<int:playlist_id>/', views.comment_playlist, name="comment_playlist"),
]
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('view_playlist/<int:playlist_id>/', views.view_playlist, name="view_playlist"),
    path('add_to_playlist/<int:entity_id>/', views.add_to_playlist, name="add_to_playlist"),
    path('delete_from_playlist/<int:entity_id>/', views.delete_from_playlist, name="delete_from_playlist"),
]
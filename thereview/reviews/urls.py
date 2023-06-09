from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('write_review/<int:entity_id>/', views.write_review, name="write_review"),
    path('view_review/<int:review_id>/', views.view_review, name="view_review"),
    path('delete_review/<int:review_id>/', views.delete_review, name="delete_review"),
]
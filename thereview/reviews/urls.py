from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('write_review/<int:entity_id>/', views.write_review, name="write_review"),
    path('view_review/<int:review_id>/', views.view_review, name="view_review"),
    path('delete_review/<int:review_id>/', views.delete_review, name="delete_review"),
    path('like_review/<int:review_id>/', views.like_review, name="like_review"),
    path('edit_blurb/<int:review_id>/', views.edit_blurb, name="edit_blurb"),
    path('comment_review/<int:review_id>/', views.comment_review, name="comment_review"),
    path('delete_review_comment/<int:review_comment_id>/', views.delete_review_comment, name="delete_review_comment"),
]
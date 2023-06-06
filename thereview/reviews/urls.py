from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('write_review/<int:entity_id>/', views.write_review, name="write_review"),
]
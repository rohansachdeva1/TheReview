from django.urls import path, re_path, include
from . import views

# ...search/_____
urlpatterns = [
    re_path(r'^', views.search_entities, name="search_entities"),
]
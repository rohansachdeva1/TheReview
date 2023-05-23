from django.urls import path, re_path, include
from . import views

# ...search/_____
urlpatterns = [
    # login
    re_path(r'^login', views.login, name="login")
    # create account
]
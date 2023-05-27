from django.urls import path, re_path, include
from . import views

# ...users/_____
urlpatterns = [
    # login
    re_path(r'^register/$', views.register, name="register"),
    re_path(r'^login/$', views.log_in, name="login"),
    re_path(r'^logout/$', views.log_out, name="logout"),
    re_path(r'^profile/$', views.view_profile, name="view_profile"),
    # create account
]
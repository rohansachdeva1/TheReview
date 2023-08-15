from django.urls import path, re_path, include
from . import views

# ...users/_____
urlpatterns = [
    # login
    re_path(r'^register/$', views.register, name="register"),
    re_path(r'^login/$', views.log_in, name="login"),
    re_path(r'^logout/$', views.log_out, name="logout"),
    path('profile/<str:username>/', views.view_profile, name="view_profile"),
    path('follow/<int:user_id>/', views.follow, name="follow"),
    path('unfollow/<int:user_id>/', views.unfollow, name="unfollow"),
    path('seen/<int:entity_id>/', views.seen, name="seen"),
    path('edit_bio', views.edit_bio, name="edit_bio"),
    path('edit_profile_image', views.edit_profile_image, name="edit_profile_image"),
]
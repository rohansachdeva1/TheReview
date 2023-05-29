from django.contrib import admin
from .models import Profile, UserTag
from reviews.models import Review
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile

class PreferencesInline(admin.StackedInline):
    model = UserTag

class ReviewsInline(admin.StackedInline):
    model = Review

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline, PreferencesInline, ReviewsInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
#admin.site.register(Profile)

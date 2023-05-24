from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'profile_picture')
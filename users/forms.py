from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User
from posts.models import Tag



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    telegram = forms.CharField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "avatar", "country", "city", "bio", "telegram", "instagram", "tags")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "avatar", "country", "city", "bio", "telegram", "instagram", "tags")


class ProfileEditForm(UserChangeForm):
    username = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    telegram = forms.CharField(required=False)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects.all())


    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "avatar", "country", "city", "bio", "telegram", "instagram", "tags")

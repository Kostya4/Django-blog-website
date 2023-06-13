from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
import posts.forms as forms
from posts.models import Tag, Category


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    avatar = models.ImageField(
        null=True, blank=True, upload_to="avatars/", default="placeholder.png")
    bio = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    instagram = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(
        'posts.Tag', related_name="user_tags", blank=True)

    follows = models.ManyToManyField(
        'User', blank=True, related_name='followers')

    black_list = models.ManyToManyField(
        'User', blank=True, related_name='blocked_users')
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username

    def get_user_url(self):
        return reverse("blog-user", args=[self.id])

    def get_follow_url(self):
        return reverse("user-follow", args=[self.id])

    def get_blocked_user_url(self):
        return reverse("block-user", args=[self.id])

    def all_tags(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    def get_all_tags(self):
        custom_category = Category.objects.get(name="Custom")
        user_tags = self.tags.all()
        default_tags = Tag.objects.all().exclude(category=custom_category).exclude(id__in=user_tags)
        tags = list(user_tags) + list(default_tags)
        return tags

    def followers_count(self):
        return len(self.followers.all())

    def follows_count(self):
        return len(self.follows.all())



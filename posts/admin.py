from django.contrib import admin
from .models import Post, Comment, Tag, Category, PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'created', 'likes_count', 'all_tags']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'created', 'likes_count']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


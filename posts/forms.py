from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('content', 'tags')


class ImagePostForm(PostForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ('image',)


class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

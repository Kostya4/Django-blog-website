from django.db import models
from django.urls import reverse


def post_image_upload_path(instance, filename):
    return f"posts/{instance.post.id}/{filename}"


class Post(models.Model):
    content = models.TextField(max_length=5000)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField("users.User", blank=True)
    tags = models.ManyToManyField('Tag', related_name="post_tags", blank=True)

    def likes_count(self):
        return len(self.likes.all())

    def comment_count(self):
        return len(self.comments.all())

    def get_post_url(self):
        return reverse("posts-post", args=[self.id])

    def get_like_url(self):
        return reverse("post-like", args=[self.id])

    def get_follow_url(self):
        return reverse("post-follow", args=[self.id])

    def get_post_url_to_delete(self):
        return reverse("delete-post", args=[self.id])

    def list_of_commented_users(self):
        user_list = []
        for comment in self.comments.all():
            user_list.append(comment.user)
        return user_list

    def all_tags(self):
        return ", ".join([tag.name for tag in self.tags.all()])


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(null=True, blank=True,
                              upload_to=post_image_upload_path)

    def images_count(self):
        return len(self.image.all())


class Comment(models.Model):
    content = models.TextField(max_length=500)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    likes = models.ManyToManyField("users.User")

    def get_likecomment_url(self):
        return reverse("comment-like", args=[self.id])

    def likes_count(self):
        return len(self.likes.all())

    def comments_count(self):
        return len(Comment.objects.all())


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_classname(self):
        return self.name.lower().replace(" ", "-")

    class Meta:
        verbose_name = "Categorie"

    def get_category_url(self):
        return reverse("explore-category", args=[self.name.replace(" ", "-")])


class Tag(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

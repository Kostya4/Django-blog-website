from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from .forms import PostForm, ImagePostForm, PostComment
from .models import Post, Comment, Category, Tag, PostImage
from users.models import User
from django.core.paginator import Paginator


class HomeView(TemplateView):
    template_name = "blog/home.html"

    def get(self, request):
        posts = Post.objects.all().order_by('-created')[:5]
        if request.user.is_authenticated:
            followed_users = [user.id for user in request.user.follows.all()]
            users = User.objects.all().order_by(
                '-date_joined').exclude(id__in=followed_users)[:5]
        else:
            users = User.objects.all().order_by('-date_joined')[:5]
        params = {
            'posts': posts,
            "users": users
        }

        return render(request, self.template_name, params)


class SuggestionsView(TemplateView):
    template_name = "blog/suggestions.html"

    def get(self, request):
        if request.user.is_authenticated:
            followed_users = [user.id for user in request.user.follows.all()]
            users = User.objects.all().order_by('-date_joined').exclude(id__in=followed_users)
        else:
            users = User.objects.all().order_by('-date_joined')

        params = {
            'users': users,
            'title': "SUGGESTIONS"
        }
        return render(request, self.template_name, params)


class ExploreView(TemplateView):
    template_name = "blog/feed.html"

    def get(self, request):
        try:
            user_tags = request.user.tags.all()
        except Exception:
            custom_cats = Category.objects.all().filter(name='Custom')
            user_tags = Tag.objects.all().exclude(category__id__in=custom_cats)
        categories = Category.objects.all()
        try:
            taged_posts = Post.objects.all().filter(
                tags__id__in=user_tags).order_by('-created').distinct()
            all_posts = Post.objects.all().exclude(id__in=taged_posts).order_by('-created')
            posts = list(taged_posts) + list(all_posts)
        except Exception as err:
            print(err)
            posts = Post.objects.all().order_by('-created')

        page_number = request.GET.get('page')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        page_list = [i+1 for i in range(num_pages + 1)]
        big_page_list = []
        for i in range(page_obj.number - 3, page_obj.number + 2):
            if i < paginator.num_pages:
                big_page_list.append(i+1)
        params = {
            "posts": page_obj,
            "user_tags": user_tags,
            "categories": categories,
            "page_list": page_list,
            "big_page_list": big_page_list
        }

        return render(request, self.template_name, params)


class ExploreTagView(TemplateView):
    template_name = 'blog/feed.html'

    def post(self, request):
        search = request.POST['search']
        posts_by_tag = Post.objects.filter(tags_icontains=search)

        page_number = request.GET.get('page')
        paginator = Paginator(posts_by_tag, 10)
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        if num_pages < 5:
            page_list = [i+1 for i in range(num_pages)]
        else:
            page_list = [i+1 for i in range(num_pages + 1)]
        big_page_list = []
        for i in range(page_obj.number - 3, page_obj.number + 2):
            if i < paginator.num_pages:
                big_page_list.append(i+1)

        params = {
            'posts': page_obj,
            "page_list": page_list,
            "big_page_list": big_page_list,
        }

        return render(request, self.template_name, params)


class FeedView(TemplateView):
    template_name = "blog/feed.html"

    def get(self, request):
        posts = Post.objects.all().order_by('-created')
        tags = Tag.objects.all()
        categories = Category.objects.all()
        
        page_number = request.GET.get('page')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        page_list = [i+1 for i in range(num_pages + 1)]
        big_page_list = []
        for i in range(page_obj.number - 3, page_obj.number + 2):
            if i < paginator.num_pages:
                big_page_list.append(i+1)

        params = {
            "posts": page_obj,
            "tags": tags,
            "categories": categories,
            "page_list": page_list,
            "big_page_list": big_page_list
        }

        return render(request, self.template_name, params)


class FollowsView(TemplateView):
    template_name = "blog/suggestions.html"

    def get(self, request, id):
        user = User.objects.get(id=id)
        follows = user.follows.all()

        params = {
            'users': follows,
            'title': f"{user.username.upper()}'S FOLLOWS:"
        }

        return render(request, self.template_name, params)


class CreatePost(TemplateView):
    template_name = "blog/home.html"

    @method_decorator(login_required)
    def post(self, request):
        if request.method == 'POST':
            form = ImagePostForm(request.POST or None, request.FILES or None)
            files = request.FILES.getlist('image')
            file_count = len(files)
            if file_count <= 5:
                if form.is_valid():
                    new_post = form.save(commit=False)
                    new_post.user = request.user
                    new_post.save()
                    form._save_m2m()
                    for image in files:
                        PostImage.objects.create(post=new_post, image=image)
                    return redirect('posts-post', new_post.id)
                else:
                    form = ImagePostForm()
                    return render(request, self.template_name, {'form': form})
            else:
                errors_image = 'Sorry, you cannot upload more than five (5) image.'
                return render(request, self.template_name, {'form': form, 'errors_image': errors_image})


class UserView(TemplateView):
    template_name = "blog/user.html"

    def get(self, request, id):
        user = User.objects.get(id=id)
        posts = Post.objects.order_by('-created').filter(user=user)
        posts_likes = Post.objects.order_by('-created').filter(likes=user)
        user_comments = Comment.objects.order_by('-created').filter(user=user)
        comments_likes = Comment.objects.order_by(
            '-created').filter(likes=user)

        page_number = request.GET.get('page')
        paginator = Paginator(posts, 5)
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        page_list = [i + 1 for i in range(num_pages + 1)]
        big_page_list = []
        for i in range(page_obj.number - 3, page_obj.number + 2):
            if i < paginator.num_pages:
                big_page_list.append(i + 1)

        params = {
            'other_user': user,
            "posts": posts,
            "posts_likes": posts_likes,
            "user_comments": user_comments,
            "comments_likes": comments_likes,
        }
        return render(request, self.template_name, params)


class SearchView(TemplateView):
    template_name = "blog/feed.html"

    def post(self, request):
        search = request.POST['search']

        try:
            categories = Category.objects.all()
            search_list = search.split()

            keyword = search_list.pop(0)
            posts_by_content = Post.objects.filter(content__iregex=keyword)
            posts_by_user_username = Post.objects.filter(
                user__username__iregex=keyword)
            posts_by_user_first_name = Post.objects.filter(
                user__first_name__iregex=keyword)
            posts_by_user_last_name = Post.objects.filter(
                user__last_name__iregex=keyword)
            posts_by_tags = Post.objects.filter(tags__name__iregex=keyword)
            posts_by_all = posts_by_content.union(
                posts_by_user_username, posts_by_user_first_name, posts_by_user_last_name, posts_by_tags)

            if len(search_list) > 0:
                for keyword in search_list:
                    posts_by_content = Post.objects.filter(
                        content__iregex=keyword)
                    posts_by_user_username = Post.objects.filter(
                        user__username__iregex=keyword)
                    posts_by_user_first_name = Post.objects.filter(
                        user__first_name__iregex=keyword)
                    posts_by_user_last_name = Post.objects.filter(
                        user__last_name__iregex=keyword)
                    posts_by_tags = Post.objects.filter(
                        tags__name__iregex=keyword)
                    posts_of_loop = posts_by_content.union(
                        posts_by_user_username, posts_by_user_first_name, posts_by_user_last_name, posts_by_tags)
                    posts_by_all = posts_by_all.union(posts_of_loop)

            caption = f'Search results for "{search}":' if posts_by_all else f'Your search - {search} - did not match any posts.'
            count = len([post for post in posts_by_all])

            params = {
                'categories': categories,
                'posts': posts_by_all.order_by('-created'),
                'title': caption,
                'count': count,
            }

        except:
            params = {
                'title': f'Search - {search}"',
                'caption': "i can't find it..."
            }

        return render(request, self.template_name, params)


class FollowByPostView(View):

    @method_decorator(login_required)
    def post(self, request, id):
        current_post = Post.objects.get(id=id)
        new_follower = current_post.user
        followers = request.user.follows.all()

        if new_follower not in followers and new_follower != request.user:
            request.user.follows.add(new_follower)
        else:
            request.user.follows.remove(new_follower)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FollowToUserView(View):

    @method_decorator(login_required)
    def post(self, request, id):
        new_follower = User.objects.get(id=id)
        followers = request.user.follows.all()

        if new_follower not in followers and new_follower != request.user:
            request.user.follows.add(new_follower)
        else:
            request.user.follows.remove(new_follower)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BlockUserView(View):

    @method_decorator(login_required)
    def post(self, request, id):
        blocked_user = User.objects.get(id=id)
        black_list = request.user.black_list.all()

        if blocked_user not in black_list and blocked_user != request.user:
            request.user.black_list.add(blocked_user)
        else:
            request.user.black_list.remove(blocked_user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ExploreCategoryView(TemplateView):
    template_name = "blog/feed.html"

    def get(self, request, category):
        categories = Category.objects.all()
        custom_cats = Category.objects.all().filter(name='Custom')
        user_tags = Tag.objects.all().exclude(category__id__in=custom_cats)
        selected_category = Category.objects.get(
            name=category.replace("-", " "))
        tags = [tag.id for tag in selected_category.tags.all()]
        posts = Post.objects.filter(tags__id__in=tags)

        page_number = request.GET.get('page')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        if num_pages < 5:
            page_list = [i+1 for i in range(num_pages)]
        else:
            page_list = [i+1 for i in range(num_pages + 1)]
        big_page_list = []
        for i in range(page_obj.number - 3, page_obj.number + 2):
            if i < paginator.num_pages:
                big_page_list.append(i+1)

        params = {
            "posts": page_obj,
            "categories": categories,
            "page_list": page_list,
            "big_page_list": big_page_list,
            "tags": selected_category.tags.all(),
            "user_tags": user_tags
        }

        return render(request, self.template_name, params)


class FollowersView(TemplateView):
    template_name = "blog/suggestions.html"

    def get(self, request, id):
        user = User.objects.get(id=id)
        followers = user.followers.all()

        params = {
            'users': followers,
            'title': f"{user.username}'s followers"
        }

        return render(request, self.template_name, params)


class CreateComment(View):

    @method_decorator(login_required)
    def post(self, request):
        if request.method == 'POST':
            form = PostComment(request.POST)
            if form.is_valid():
                post = Post.objects.get(id=request.POST['post_id'])
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.post = post
                new_post.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                form = PostComment()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteCommentView(DeleteView):
    @method_decorator(login_required)
    def post(self, request):
        comment_on_delete = Comment.objects.get(id=request.POST['comment_id'])
        if request.user == comment_on_delete.user:
            comment_on_delete.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeletePostView(View):
    @method_decorator(login_required)
    def post(self, request, id):
        post = Post.objects.get(id=id)
        if request.user == post.user:
            post.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LikeComment(View):
    @method_decorator(login_required)
    def post(self, request, id):
        current_comment = Comment.objects.get(id=id)
        likes = [user for user in current_comment.likes.all()]
        if request.user not in likes:
            current_comment.likes.add(request.user)
        else:
            current_comment.likes.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TagSearchView(TemplateView):
    template_name = "blog/feed.html"

    def get(self, request, tag_id):
        tag = Tag.objects.get(pk=tag_id)
        posts = Post.objects.filter(tags__in=[tag_id]).order_by('-created')
        categories = Category.objects.all()

        page_number = request.GET.get('page')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        if num_pages < 5:
            page_list = [i+1 for i in range(num_pages)]
        else:
            page_list = [i+1 for i in range(num_pages + 1)]
        big_page_list = []
        for i in range(page_obj.number - 3, page_obj.number + 2):
            if i < paginator.num_pages:
                big_page_list.append(i+1)

        params = {
            'categories': categories,
            'posts': page_obj,
            'tag': tag,
            'title': f'POSTS BY TAG "{tag.name}"',
            'page_list': page_list,
            'big_page_list': big_page_list
        }

        return render(request, self.template_name, params)


class LikeView(View):

    @method_decorator(login_required)
    def post(self, request, id):
        current_post = Post.objects.get(id=id)
        likes = [user for user in current_post.likes.all()]
        if request.user not in likes:
            current_post.likes.add(request.user)
        else:
            current_post.likes.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostView(TemplateView):
    template_name = "blog/post_detail.html"

    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
            comment = Comment.objects.filter(post=post)
            params = {
                'post': post,
                'comment': comment,
            }
            return render(request, self.template_name, params)
        except:
            return redirect('blog-user', request.user.id)

from django.urls import path
from .views import HomeView, PostView, SuggestionsView, CreatePost, FeedView, UserView, SearchView, LikeView,\
    ExploreView, FollowByPostView, FollowToUserView, FollowsView, FollowersView, ExploreCategoryView, CreateComment, DeleteCommentView, \
    DeletePostView, LikeComment, TagSearchView, BlockUserView

from django.views.decorators.cache import cache_page

urlpatterns = [
    path("", HomeView.as_view(), name="posts-home"),
    path("feed/", FeedView.as_view(), name="feed-index"),
    path("explore/", ExploreView.as_view(), name="explore-index"),
    path("suggestions/", SuggestionsView.as_view(), name="posts-suggestions"),
    path("create_post/", CreatePost.as_view(), name="post-create"),
    path("blog/user-<int:id>/", UserView.as_view(), name="blog-user"),
    path("search/", SearchView.as_view(), name='post-search'),
    path("posts/post-<int:id>/", PostView.as_view(), name="posts-post"),
    path("posts/post-<int:id>/", PostView.as_view(), name="posts-post"),
    path("posts/like-<int:id>/", LikeView.as_view(), name="post-like"),
    path("posts/comment/like-<int:id>/", LikeComment.as_view(), name="comment-like"),
    path("posts/user/block/user-<int:id>/", BlockUserView.as_view(), name="block-user"),
    path("posts/post/follow-<int:id>/", FollowByPostView.as_view(), name="post-follow"),
    path("posts/user/follow-<int:id>/", FollowToUserView.as_view(), name="user-follow"),
    path('explore/category-<str:category>/', ExploreCategoryView.as_view(), name="explore-category"),
    path("user-<int:id>/followers/", FollowersView.as_view(), name="user-followers"),
    path("user-<int:id>/follows/", FollowsView.as_view(), name="user-follows"),
    path("create_comment/", CreateComment.as_view(), name="comment-create"),
    path("delete_comment/", DeleteCommentView.as_view(), name='comment-delete'),
    path("posts/post/post_delete-<int:id>", DeletePostView.as_view(), name="delete-post"),
    path("posts/by-tags/<int:tag_id>/", TagSearchView.as_view(), name="search-by-tag"),
]

from django.urls import path
from .views import FollowView, UserList, PostList, UserDetail, RegistrationUserView, LoginView, LogoutView, PostDetailView

urlpatterns = [
    path('users/', UserList.as_view(), name='api-users'),
    path('users/follow/<int:pk>/', FollowView.as_view({'post': 'follow'}), name='api-follow'),
    path('users/unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'}), name='api_unfollow'),
    path('posts/', PostList.as_view(), name="api-posts"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='api-post-detail'),
    path('users/<int:pk>', UserDetail.as_view(), name="api-user-detail"),
    path('registration/', RegistrationUserView.as_view(), name='api_registration'),
    path("login/", LoginView.as_view(), name="api-login"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
]

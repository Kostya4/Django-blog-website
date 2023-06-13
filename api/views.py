from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from users.models import User
from . import serializers
from .serializers import UserRegistrationSerializer, UserSerializer
from posts.models import Post


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(APIView):

    @permission_classes([IsAuthenticated])
    def post(self, request):
        logout(request)
        return Response('User Logged out successfully', status=status.HTTP_200_OK)


class RegistrationUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['user_id'] = user.id
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class FollowView(viewsets.ViewSet):

    def follow(self, request, pk):
        user = request.user
        following_user = User.objects.get(id=pk)
        if user != following_user:
            user.follows.add(following_user)
            return Response({'message': 'Now you are following this user'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def unfollow(self, request, pk):
        user = request.user
        following_user = User.objects.get(id=pk)
        if user != following_user:
            user.follows.remove(following_user)
            return Response({'message': 'now you are not following this user'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "you can't stop following yourself"}, status=status.HTTP_400_BAD_REQUEST)


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

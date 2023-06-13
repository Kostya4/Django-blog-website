from rest_framework import serializers, viewsets
from posts.models import Post
from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def save(self):
        user = User(
            username=self.validated_data.get('username'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            email=self.validated_data.get('email')
        )
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        user.set_password(password)
        user.save()
        return user
        
        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'avatar', 'city', 'country', 'bio', 'instagram', 'telegram', 'is_staff', 'is_active']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content', 'user', 'created', 'likes_count', 'comment_count']

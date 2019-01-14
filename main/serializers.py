from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'name', 'create_time', 'text')

    def get_name(self, obj):
        return obj.owner.profile.nickname


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'create_time', 'image', 'text', 'like_count')

    def get_like_count(self, obj):
        return obj.like.all().count()

    def get_author_name(self, obj):
        return obj.owner.profile.nickname


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    who_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'create_time', 'image', 'comments', 'text', 'who_like')
        depth = 1

    def get_who_like(self, obj):
        print(obj.like.all())
        return [owner.profile.nickname for owner in obj.like.all()]

    def get_author_name(self, obj):
        return obj.owner.profile.nickname


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname')

    def get_nickname(self, obj):
        return obj.profile.nickname

from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Comment
        fields = ('id', 'name', 'create_time', 'text')

    def get_user_name(self, obj):
        return obj.author.profile.nickname


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'create_time', 'image', 'text', 'like_count')

    def get_like_count(self, obj):
        return obj.like.all().count()

    def get_author_name(self, obj):
        return obj.author.profile.nickname


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    who_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'create_time', 'image', 'comments', 'text', 'who_like')
        depth = 1

    def get_who_like(self, obj):
        print(obj.like.all())
        return [user.profile.nickname for user in obj.like.all()]

    def get_author_name(self, obj):
        return obj.author.profile.nickname

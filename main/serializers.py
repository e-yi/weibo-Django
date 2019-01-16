from rest_framework import serializers
from .models import *


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    # create_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Comment
        fields = ('id', 'name', 'create_time', 'text')

    def get_name(self, obj):
        return obj.owner.profile.nickname


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    # create_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    image = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'create_time', 'image', 'text', 'like_count', 'comment_count')

    def get_like_count(self, obj):
        return obj.like.all().count()

    def get_comment_count(self, obj):
        return obj.comments.all().count()

    def get_author_name(self, obj):
        return obj.owner.profile.nickname


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    who_like = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author_name', 'create_time', 'image', 'comments', 'text', 'who_like')
        depth = 1

    def get_who_like(self, obj):
        return [owner.profile.nickname for owner in obj.like.all()]

    def get_author_name(self, obj):
        return obj.owner.profile.nickname


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'nickname')

    def get_username(self, obj):
        return obj.owner.username

class CreateUserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=15, write_only=True)

    class Meta:
        model = User
        fields = ('nickname', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        user.profile.nickname = validated_data['nickname']
        user.profile.save() # or just call user.save()
        return user

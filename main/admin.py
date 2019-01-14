from django.contrib import admin
from .models import *


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'nickname', 'gender', 'location')
    list_filter = ('gender',)
    search_fields = ('nickname',)

    def get_user(self, obj):
        return obj.user.id

    get_user.short_description = 'userId'
    get_user.admin_order_field = 'user__id'


class PostAdmin(admin.ModelAdmin):
    list_display = ('get_author', 'create_time', 'modify_time', 'image', 'text')

    def get_author(self, obj):
        return obj.author.profile.nickname

    get_author.short_description = 'author'
    get_author.admin_order_field = 'author__nickname'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_author', 'text', 'create_time')

    def get_author(self, obj):
        return obj.author.profile.nickname

    get_author.short_description = 'author'
    get_author.admin_order_field = 'author__nickname'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

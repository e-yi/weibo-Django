from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # use user create to create
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # use user.save to save
    instance.profile.save()


class Profile(models.Model):
    """
    个人资料，包括：
    出生日期、个人简介、昵称、所在地、性别、关注、被关注
    账户创建日期
    """
    GENDER_ITEMS = [
        (1, '男'),
        (2, '女'),
        (0, '未知')
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=15, blank=False, default="user", verbose_name='昵称')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    location = models.CharField(max_length=30, blank=True, verbose_name='所在地')
    birth_date = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.IntegerField(choices=GENDER_ITEMS, blank=True, verbose_name='性别', default=0)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")
    follows = models.ManyToManyField('self', related_name='follower', symmetrical=False,
                                     verbose_name='关注', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '个人资料'


class Post(models.Model):
    """
    微博，包括：
    作者、发布时间、修改时间、文字、图片、点赞数
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    create_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    image = models.ImageField(blank=True, verbose_name="图片", upload_to='post_image')
    text = models.TextField(max_length=180, verbose_name="文字")
    like = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '微博'


class Comment(models.Model):
    """
    评论，包括：
    作者，评论对象，评论时间，文字
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    to = models.ForeignKey(Post, on_delete=models.CASCADE,
                           verbose_name="微博", related_name='comments')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    text = models.TextField(max_length=90, verbose_name="文字")

    class Meta:
        verbose_name = verbose_name_plural = '评论'

@receiver(post_delete, sender=Post)
def photo_post_delete_handler(sender, **kwargs):
    """
    当删除微博时删除对应图片
    """
    photo = kwargs['instance']
    try:
        storage, path = photo.image.storage, photo.image.path
        storage.delete(path)
    except ValueError as e:
        print(e)
        pass



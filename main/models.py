from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Create your models here.
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15, blank=False,default="user")
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    location = models.CharField(max_length=30, blank=True, verbose_name='所在地')
    birth_date = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.IntegerField(choices=GENDER_ITEMS, blank=True, verbose_name='性别')
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")
    follows = models.ManyToManyField('self', related_name='follows', symmetrical=False)

    class Meta:
        verbose_name = verbose_name_plural = '个人资料'


class Post(models.Model):
    """
    微博，包括：
    作者、发布时间、修改时间、文字、图片、点赞数、
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)


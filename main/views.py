from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view


@api_view(['GET'])
def weibo_info(request):
    """
    获取基本信息
    """

@api_view(['GET'])
def weibo_list(request):
    """
    获取微博列表
    """
    pass


@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def weibo(request):
    """
    微博详情及该微博的评论
    增删改查
    """
    pass


@api_view(['POST', 'DELETE'])
def comment(request):
    """
    添加评论
    增删
    """

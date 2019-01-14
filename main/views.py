from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


# TODO 增加用户认证
# TODO 填充view

@api_view(['GET'])
def weibo_info(request):
    """
    获取基本信息
    """
    data = {}
    data['weibo_count'] = Post.objects.count()
    return Response(data=data)


@api_view(['GET'])
def weibo_list(request, start=-1, n=20):
    """
    获取微博列表
    @:param start 从微博id=start开始
    @:param len 总共接受n个微博
    """
    if start == -1:
        posts = Post.objects.order_by('-id')[:n]
    else:
        posts = Post.objects.filter('id__lte=' + str(start)).order_by('-id')[:n]
    serializer = PostSerializer(posts, many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
def create_weibo(request):
    pass  # TODO


class weibo(generics.RetrieveUpdateDestroyAPIView):
    """
    微博详情及该微博的评论 : 查
    微博 : 删改
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


@api_view(['POST'])
def create_comment(request):
    pass  # TODO


class comment(generics.DestroyAPIView):
    """
    评论:删
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

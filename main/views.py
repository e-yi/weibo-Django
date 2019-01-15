from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main.permissions import IsOwnerOrReadOnly
from .serializers import *


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
        posts = Post.objects.filter(id__lte=start).order_by('-id')[:n]
    serializer = PostSerializer(posts, many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_weibo(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Weibo(generics.RetrieveUpdateDestroyAPIView):
    """
    微博详情及该微博的评论 : 查
    微博 : 删改
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(generics.DestroyAPIView):
    """
    评论:删
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


# TODO
@api_view(['POST'])
def create_user(request):
    pass


# TODO
@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def like(request, pk):
    """
    点赞
    """
    pass

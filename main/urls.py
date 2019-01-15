from django.urls import path, include
from . import views

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('info',
         views.weibo_info),
    path('user_info',
         views.UserInfo.as_view()),
    path('user_info/<int:pk>',
         views.UpdateUserInfo.as_view()),
    path('weibo/list',
         views.weibo_list),
    path('weibo/list/<int:start>/<int:n>',
         views.weibo_list),
    path('weibo',
         views.create_weibo),
    path('weibo/<int:pk>',
         views.Weibo.as_view()),
    path('weibo/<int:pk>/comment',
         views.create_comment),
    path('weibo/<int:pk>/like',
         views.like),
    path('comment/<int:pk>',
         views.Comment.as_view()),
]

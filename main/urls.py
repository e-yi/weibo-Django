from django.urls import path, include
from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('info',
         views.weibo_info),
    path('weibo/list/',
         views.weibo_list),
    path('weibo/list/<int:start>/<int:n>',
         views.weibo_list),
    path('weibo',
         views.create_weibo),
    path('weibo/<int:pk>',
         views.weibo.as_view()),
    path('weibo/<int:pk>/comment',
         views.create_comment),
    path('comment/<int:pk>',
         views.comment.as_view()),
]

from django.urls import path
from . import views

urlpatterns = [
    path('weibo/',
         views.weibo_info),
    path('weibo/list/',
         views.weibo_list),
    path('weibo/list/<int:from>/<int:to>',
         views.weibo_list),
    path('weibo/<int:pk>',
         views.weibo),
    path('comment/<int:pk>',
         views.comment),
]

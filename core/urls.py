# urls.py

from django.urls import path
from . import views
from .views import (ArticleCreateAPIView, ArticleListAPIView, CreateVideoAPIView,
          SingleArticleAPIView, CategoryCreateAPIView, SingleCategoryAPIView, 
          CreateCommentAPIView,
          SingleCommentAPIView, SingleVideoAPIView, VideoListAPIView)

urlpatterns = [
########################################-ARTICLE URLS-######################################################
#crete,listing all and select single ARTICLES VIEWS
    path('add-categories/', CategoryCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', SingleCategoryAPIView.as_view(), name='category-detail'),

#crete,listing all and select single ARTICLES VIEWS
    path('add-article/', ArticleCreateAPIView.as_view(), name='article-list-create'),
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('article/<int:pk>/', SingleArticleAPIView.as_view(), name='article-detail'),

#crete,listing all and select single ARTICLES VIEWS
    path('add-comments/', CreateCommentAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', SingleCommentAPIView.as_view(), name='comment-detail'),
########################################-VIDEO urls-######################################################
    path('add-video/', CreateVideoAPIView.as_view(), name='video-list-create'),
    path('videos/', VideoListAPIView.as_view(), name='video-list'),
    path('video/<int:pk>/', SingleVideoAPIView.as_view(), name='video-detail'),

    #community urls
    path('communities/', views.CommunityList.as_view(), name='community-list'),
    path('communities/create/', views.CommunityCreate.as_view(), name='community-create'),
    path('communities/<int:pk>/', views.CommunityDetail.as_view(), name='community-detail'),
    ##post
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    ##reply
    path('replies/', views.ReplyList.as_view(), name='reply-list'),
    path('replies/create/', views.ReplyCreate.as_view(), name='reply-create'),
    path('reply/<int:pk>/', views.ReplyDetail.as_view(), name='reply-detail'),
]

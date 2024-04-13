from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ( 
    addArticle, addcategory, articleList, categorylist, dashboard, addVideo, delete_category, edit_category, video_detail,
    video_list,community_list,
    user_list,
    add_user,
    adminlogin,forgot_password, view_profile
    # delete_video,
    # edit_video,
    # delete_user,
    # edit_user,
    
)

urlpatterns = [

   
    path('', dashboard, name='dashboard'),
    path('add-video/', addVideo, name='add-video'),
    path('video_list/', video_list, name='video_list'),
    path('videos/<int:video_id>/', video_detail, name='video_detail'),
    path('add-category/', addcategory, name='add-category'),
    path('categorylist/', categorylist, name='categorylist'),
    path('edit_category/<int:category_id>/', edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),


    path('add-article/', addArticle, name='add-article'),
    path('article_list/', articleList, name='article_list'),

    path('add-community/', addArticle, name='add-community'),
    path('community_list/', community_list, name='community_list'),

    

    path('user_list/', user_list, name='user_list'),
    path('add_user/', add_user, name='add_user'),
    
    path('profile/', view_profile, name='view_profile'),
    # path('profile/edit/', edit_profile, name='edit_profile'),
    # path('dashboard/video/<int:video_id>/edit/', edit_video, name='edit_video'),
    # path('dashboard/video/<int:video_id>/delete/', delete_video, name='delete_video'),
    # path('dashboard/user/<int:user_id>/', delete_user, name='delete_user'),
    # path('dashboard/edit_user/<int:user_id>/', edit_user, name='edit_user'),

    path('', adminlogin, name='adminlogin'),
    path('forget-password', forgot_password , name='forget-password'),

     
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
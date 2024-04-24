# urls.py

from django.urls import path
from . import views
from .views import (ArticleCreateAPIView, ArticleListAPIView, CreateVideoAPIView,
          SingleArticleAPIView, CategoryCreateAPIView, SingleCategoryAPIView, 
          CreateCommentAPIView,
          SingleCommentAPIView, SingleVideoAPIView, VideoListAPIView,AssignmentCreateAPIView, 
          AssignmentDetailAPIView, AssignmentListAPIView, ChapterCreateAPIView, ChapterDetailAPIView, 
          ChapterListAPIView, ChoiceCreateAPIView,ChoiceDetailAPIView, ChoiceListAPIView, CourseCreateAPIView, 
          CourseListAPIView, CourseDetailAPIView, LectureCreateAPIView,LectureDetailAPIView, LectureListAPIView,
          QuestionCreateAPIView, QuestionDetailAPIView, QuestionListAPIView,QuizCreateAPIView, 
          QuizDetailAPIView, QuizListAPIView, SubmissionCreateAPIView, SubmissionDetailAPIView, 
          SubmissionListAPIView)

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
    
    ##Courses
    path('courses/', CourseListAPIView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    ##Chapeter
    path('chapters/', ChapterListAPIView.as_view(), name='chapter-list'),
    path('course/<int:course_id>/chapters/create/', ChapterCreateAPIView.as_view(), name='chapter-create'),
    path('chapters/<int:pk>/', ChapterDetailAPIView.as_view(), name='chapter-detail'),
    ##Lectures
    path('lectures/', LectureListAPIView.as_view(), name='lecture-list'),
    path('chapters/<int:chapter_id>/lectures/create/', LectureCreateAPIView.as_view(), name='lecture-create'),
    path('lectures/<int:pk>/', LectureDetailAPIView.as_view(), name='lecture-detail'),
    ##Quiz
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('courses/<int:course_id>/quizzes/create/', QuizCreateAPIView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    ##questions
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('quizzes/<int:quiz_id>/questions/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='question-detail'),
    ##answers/choices
    path('choices/', ChoiceListAPIView.as_view(), name='choice-list'),
    path('questions/<int:question_id>/choices/create/', ChoiceCreateAPIView.as_view(), name='choice-create'),
    path('choices/<int:pk>/', ChoiceDetailAPIView.as_view(), name='choice-detail'),
    #assignments
    path('assignments/', AssignmentListAPIView.as_view(), name='assignment-list'),
    path('courses/<int:course_id>/assignments/create/', AssignmentCreateAPIView.as_view(), name='assignment-create'),
    path('assignments/<int:pk>/', AssignmentDetailAPIView.as_view(), name='assignment-detail'),
    ##submittions
    path('submissions/', SubmissionListAPIView.as_view(), name='submission-list'),
    path('submissions/create/', SubmissionCreateAPIView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', SubmissionDetailAPIView.as_view(), name='submission-detail'),


##special for quiz
#     path('quiz/<int:quiz_id>/', QuizAPIView.as_view(), name='quiz-detail'),
#     path('question/<int:question_id>/', QuestionAPIView.as_view(), name='question-detail'),
]


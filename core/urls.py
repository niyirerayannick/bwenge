# urls.py

from django.urls import path
from . import views
from .views import (ArticleCreateAPIView, ArticleListAPIView, AssignUsersToSPOCAPIView, CommunityStarView,
                     CourseEnrollAPIView, CreateVideoAPIView, EventCreateView, EventDetailView, InstitutionDetail, InstitutionList, 
                     JoinCommunityView, LiveEventsView,  MyArticlesView, MyCoursesView, MyProjectsView, 
                     MyStatisticsView, ProjectDeleteView, ProjectDetailView, ProjectDownloadView, ProjectListView, ProjectUpdateView,SingleArticleAPIView, CategoryCreateAPIView,
                     SingleCategoryAPIView,  CreateCommentAPIView,SingleCommentAPIView, SingleVideoAPIView, TakeQuizAPIView,
                       ToggleLikeView, UploadExcelAPIView, VideoListAPIView,AssignmentCreateAPIView, 
          AssignmentDetailAPIView, AssignmentListAPIView, ChapterCreateAPIView, ChapterDetailAPIView, 
          ChapterListAPIView, ChoiceCreateAPIView,ChoiceDetailAPIView, ChoiceListAPIView,
          CourseCreateAPIView, CourseListAPIView, CourseDetailAPIView, LectureCreateAPIView,
          LectureDetailAPIView, LectureListAPIView, QuestionCreateAPIView, QuestionDetailAPIView, 
          QuestionListAPIView,QuizCreateAPIView,  QuizDetailAPIView, QuizListAPIView, SubmissionCreateAPIView,
          SubmissionDetailAPIView, SubmissionListAPIView, WaitingEventsView, mycommunuties, ProjectCreateView)

urlpatterns = [
########################################-ARTICLE URLS-######################################################
#crete,listing all and select single ARTICLES VIEWS
    path('add-categories/', CategoryCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', SingleCategoryAPIView.as_view(), name='category-detail'),

#crete,listing all and select single ARTICLES VIEWS
    path('add-article/', ArticleCreateAPIView.as_view(), name='article-list-create'),
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('article/<int:pk>/', SingleArticleAPIView.as_view(), name='article-detail'),
    # path('article/<int:pk>/like/', LikeArticleView.as_view(), name='article-like'),  # New endpoint for liking
    path('article/like/', ToggleLikeView.as_view(), name='toggle-like'),

#crete,listing all and select single ARTICLES VIEWS
    path('add-comments/', CreateCommentAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', SingleCommentAPIView.as_view(), name='comment-detail'),
########################################-VIDEO urls-#####################################################

    #community urls
    path('communities/', views.CommunityList.as_view(), name='community-list'),
    path('communities/create/', views.CommunityCreate.as_view(), name='community-create'),
    path('communities/<int:pk>/', views.CommunityDetail.as_view(), name='community-detail'),
    path('communities/<int:pk>/edit/', views.CommunityUpdate.as_view(), name='community-update'),  # Edit community
    path('communities/<int:pk>/delete/', views.CommunityDelete.as_view(), name='community-delete'),  # Delete community

    path('communities/categories', views.Commu_categoryCreateAPIView.as_view(), name='community-categories-list'),
    path('communities/<int:community_id>/join/', JoinCommunityView.as_view(), name='community-join'),
    path('communities/<int:community_id>/stars/', CommunityStarView.as_view(), name='community_star'),
    #All for single user
    path('my-communities/', mycommunuties.as_view(), name='my-communities'),
    path('my-articles/', MyArticlesView.as_view(), name='my-articles'),
    path('my-projects/', MyProjectsView.as_view(), name='my-projects'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('mystatistics/', MyStatisticsView.as_view(), name='mystatistics'),

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
    path('courses/<int:course_id>/take/', CourseEnrollAPIView.as_view(), name='course-enroll'),
    path('courses/<int:course_id>/assign/', AssignUsersToSPOCAPIView.as_view(), name='assign-users-to-spoc'),
    path('courses/<int:course_id>/upload_excel/', UploadExcelAPIView.as_view(), name='upload-excel'),
    ##Chapeter   fer xzyvg frc
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
    path('quizzes/<int:quiz_id>/take/', TakeQuizAPIView.as_view(), name='take-quiz'),
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
    #projects
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/<int:pk>/download/', ProjectDownloadView.as_view(), name='project-download'),


    #institutions
    path('institutions/', InstitutionList.as_view(), name='institution-list'),
    path('institutions/<int:pk>/', InstitutionDetail.as_view(), name='institution-detail'),
    #Nsangiza
    path('nsangiza/event/create/', EventCreateView.as_view(), name='event-create'),
    path('nsangiza/events/waiting/', WaitingEventsView.as_view(), name='waiting-events'),
    path('nsangiza/events/live/', LiveEventsView.as_view(), name='live-events'),
    path('nsangiza/event/<int:id>/', EventDetailView.as_view(), name='event-detail'),
    path('nsangiza/video/create', CreateVideoAPIView.as_view(), name='video-list-create'),
    path('nsangiza/video/list', VideoListAPIView.as_view(), name='video-list'),
    path('nsangiza/video/<int:pk>/', SingleVideoAPIView.as_view(), name='video-detail'),
]
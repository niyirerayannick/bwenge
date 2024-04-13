from django.urls import path
from .views import (AssignmentCreateAPIView, AssignmentDetailAPIView, AssignmentListAPIView, ChapterCreateAPIView, ChapterDetailAPIView, 
                    ChapterListAPIView, ChoiceCreateAPIView,
                    ChoiceDetailAPIView, ChoiceListAPIView, CourseCreateAPIView, 
                    CourseListAPIView, CourseDetailAPIView, LectureCreateAPIView,
                    LectureDetailAPIView, LectureListAPIView,
                    QuestionCreateAPIView, QuestionDetailAPIView, QuestionListAPIView,
                    QuizCreateAPIView, QuizDetailAPIView, QuizListAPIView, SubmissionCreateAPIView, SubmissionDetailAPIView, SubmissionListAPIView)

urlpatterns = [
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
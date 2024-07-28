# views.py
from turtle import pd
from django.shortcuts import get_object_or_404
import openpyxl
from rest_framework import status
import logging
from django.apps import apps
from django.conf import settings
from accounts.models import User
from accounts.utils import send_course_assignment_email
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics,status
from .models import (Article, Comment,Category, Community, CommunityCategory, Enrollment, PendingEnrollment, Post, Reply,Video,Project,
                     Assignment, Chapter, Choice, Course, Lecture, Question, Quiz, Submission,
                     Quiz, Question, Choice)
from .serializers import (ArticleSerializer, CategorySerializer, CommentSerializer, CommunityCategorySerializer, 
                          CommunitySerializer, EmailAssignmentSerializer, EnrollmentSerializer, JoinCommunitySerializer,
                            PostSerializer, ReplySerializer, ProjectSerializer, TakeQuizSerializer, UploadExcelSerializer,
                          VideoSerializer,CourseSerializer,AssignmentSerializer, ChapterSerializer,
                            ChoiceSerializer, CourseSerializer,LectureSerializer, QuestionSerializer,
                              QuizSerializer, SubmissionSerializer,QuizSerializer, QuestionSerializer)

########################################-ARTICLES VIEWS-######################################################

#crete,listing all and select single CATEGORIES
class CategoryCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#crete,listing all and select single ARTICLES VIEWS
class ArticleCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        # Order articles by 'created_at' field in descending order
        return Article.objects.all().order_by('-created_at')

class SingleArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  #increment views count
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#crete,listing all and select single COMMENTS
class CreateCommentAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class SingleCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

########################################-VIDEO VIEWS-######################################################

class CreateVideoAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class SingleVideoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # Increment views count
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
########################################-community VIEWS-######################################################
class CommunityList(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityCreate(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityDetail(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

from rest_framework.permissions import AllowAny
class JoinCommunityView(APIView):
    permission_classes = [AllowAny]  # Adjust if necessary for your authentication needs

    def post(self, request, community_id, format=None):
        serializer = JoinCommunitySerializer(data={'community_id': community_id})
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None

            # Check if user is authenticated
            if user is None:
                return Response({'error': 'User must be logged in to join a community.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve the community instance
            try:
                community = Community.objects.get(id=community_id)
            except Community.DoesNotExist:
                return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Check if user is already a member of the community
            if community.members.filter(id=user.id).exists():
                return Response({'message': 'You are already a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)

            # Add user to the community
            community.members.add(user)
            
            return Response({
                'community_id': community.id,
                'message': 'Successfully joined the community'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Commu_categoryCreateAPIView(generics.ListCreateAPIView):
    queryset = CommunityCategory.objects.all()
    serializer_class = CommunityCategorySerializer

########################################-MY community-######################################################

class mycommunuties(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter communities by the logged-in user's ID
        communities = Community.objects.filter(admin=request.user)
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyArticlesView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return articles that are authored by the currently logged-in user
        return Article.objects.filter(author=self.request.user)
    
class MyProjectsView(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return projects that are authored by the currently logged-in user
        return Project.objects.filter(author=self.request.user)

class MyCoursesView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Returns courses that are created by the currently logged-in user
        return Course.objects.filter(teacher=self.request.user)

class MyStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_communities = Community.objects.filter(admin=request.user).count()
        total_articles = Article.objects.filter(author=request.user).count()
        total_projects = Project.objects.filter(author=request.user).count()
        total_courses = Course.objects.filter(teacher=request.user).count()
        
        response_data = {
            'total_communities': total_communities,
            'total_articles': total_articles,
            'total_projects': total_projects,
            'total_courses': total_courses
        }
        return Response(response_data, status=status.HTTP_200_OK)

##post
class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#reply

class ReplyList(generics.ListAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class ReplyCreate(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class ReplyDetail(generics.RetrieveAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

##coursea
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # Set the default course type to 'mooc' if not provided
        course_type = self.request.data.get('course_type', 'mooc')
        # Save the course with the provided teacher and course_type
        serializer.save(course_type=course_type)


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        # Order courses by 'id' field in descending order
        return Course.objects.all().order_by('-id')

class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# ###chapters
class ChapterCreateAPIView(generics.CreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def perform_create(self, serializer):
        # Ensure that the course_id is provided in the request data
        serializer.save(course_id=self.kwargs['course_id'])

class ChapterListAPIView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class ChapterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

###Lectures
class LectureCreateAPIView(generics.CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def perform_create(self, serializer):
        # Ensure that the chapter_id is provided in the request data
        serializer.save(chapter_id=self.kwargs['chapter_id'])

class LectureListAPIView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    

##Quiz
    
class QuizCreateAPIView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        # Ensure that the course_id is provided in the request data
        serializer.save(course_id=self.kwargs['course_id'])

class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class TakeQuizAPIView(generics.CreateAPIView):
    serializer_class = TakeQuizSerializer

    def post(self, request, *args, **kwargs):
        quiz_id = self.kwargs.get('quiz_id')
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        # Pass the user and quiz to the serializer
        serializer = self.get_serializer(data=request.data, context={'request': request, 'quiz': quiz, 'user': user})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response(result, status=status.HTTP_201_CREATED)
##questions
    
class QuestionCreateAPIView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        # Ensure that the quiz_id is provided in the request data
        serializer.save(quiz_id=self.kwargs['quiz_id'])

class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

##answers/choice becouse we use multiple choice question on quizzes
class ChoiceCreateAPIView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        # Ensure that the question_id is provided in the request data
        serializer.save(question_id=self.kwargs['question_id'])

class ChoiceListAPIView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer   

##assigments

class AssignmentCreateAPIView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        # Ensure that the course_id is provided in the request data
        serializer.save(course_id=self.kwargs['course_id'])

class AssignmentListAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class SubmissionCreateAPIView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Pass the user to the serializer context
        serializer = self.get_serializer(data=request.data, context={'user_id': user.id, 'view': self})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SubmissionListAPIView(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer



class SubmissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_object(self):
        """
        Optionally restrict the returned submission to the submissions related to the
        currently authenticated user.
        """
        obj = super().get_object()
        if obj.student != self.request.user:
            self.permission_denied(self.request)
        return obj



class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     # Automatically set the author to the logged in user during project creation
    #     serializer.save(author=self.request.user)

class CourseEnrollAPIView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({"error": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(user=user, course=course)
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class EnrollmentListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user, authenticated or not

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)
    
class TakeCourseAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user, authenticated or not

    def post(self, request, course_id, *args, **kwargs):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if course.course_type == 'mooc':
            if Enrollment.objects.filter(user=user, course=course).exists():
                return Response({'detail': 'You are already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
            enrollment = Enrollment.objects.create(user=user, course=course)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'detail': 'Cannot self-enroll in SPOC courses.'}, status=status.HTTP_403_FORBIDDEN)

class AssignUsersToSPOCAPIView(APIView):
    def post(self, request, course_id):
        serializer = EmailAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            emails = serializer.validated_data['emails']
            course = Course.objects.get(id=course_id)  # Get the course instance
            already_assigned_emails = []
            newly_assigned_emails = []
            
            User = apps.get_model(settings.AUTH_USER_MODEL)  # Get the actual user model
            
            for email in emails:
                user = User.objects.filter(email=email).first()  # Check if the user exists
                if user:
                    if Enrollment.objects.filter(user=user, course=course).exists():
                        already_assigned_emails.append(email)
                    else:
                        # Enroll the existing user in the course
                        Enrollment.objects.create(user=user, course=course)
                        newly_assigned_emails.append(email)
                else:
                    # Create a pending enrollment record for users who do not exist yet
                    PendingEnrollment.objects.create(email=email, course=course)
                    newly_assigned_emails.append(email)
            
            response_data = {
                'already_assigned_emails': already_assigned_emails,
                'newly_assigned_emails': newly_assigned_emails,
                'message': 'Courses assigned successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadExcelAPIView(APIView):
    def post(self, request, course_id):
        serializer = UploadExcelSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            
            try:
                workbook = openpyxl.load_workbook(excel_file)
                sheet = workbook.active
                
                emails = set()
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    email = row[0]
                    if email:
                        emails.add(email)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            course = Course.objects.get(id=course_id)
            already_assigned_emails = []
            newly_assigned_emails = []
            
            User = apps.get_model(settings.AUTH_USER_MODEL)
            
            for email in emails:
                user = User.objects.filter(email=email).first()
                if user:
                    if Enrollment.objects.filter(user=user, course=course).exists():
                        already_assigned_emails.append(email)
                    else:
                        Enrollment.objects.create(user=user, course=course)
                        newly_assigned_emails.append(email)
                        send_course_assignment_email(email, course.title, request)  # Send email to the user
                else:
                    PendingEnrollment.objects.create(email=email, course=course)
                    newly_assigned_emails.append(email)
            
            response_data = {
                'already_assigned_emails': already_assigned_emails,
                'newly_assigned_emails': newly_assigned_emails,
                'message': 'Courses assigned and emails attempted'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
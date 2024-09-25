# views.py
from turtle import pd
from .models import Event
from .serializers import EventCreateSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import openpyxl
from rest_framework import status
import logging
from rest_framework.exceptions import ValidationError
from django.apps import apps
from django.conf import settings
from accounts.models import User
from accounts.utils import send_course_assignment_email
from django.db.models import Count
from core import serializers
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics,status
from .models import (Article, ArticleLike, Comment,Category, Community, CommunityCategory, Enrollment, 
                     Institution,PendingEnrollment, Post, Reply,Video,Project,
                     Assignment, Chapter, Choice, Course, Lecture, Question, Quiz, Submission,
                     Quiz, Question, Choice)
from .serializers import (ArticleSerializer, CategorySerializer, CommentSerializer, CommunityCategorySerializer, 
                          CommunitySerializer,EmailAssignmentSerializer, EnrollmentSerializer, EventSerializer,
                            InstitutionSerializer, JoinCommunitySerializer,
                            PostSerializer, ReplySerializer, ProjectSerializer, TakeQuizSerializer, ToggleLikeSerializer, 
                            UploadExcelSerializer, UserSerializer,
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

    def create(self, request, *args, **kwargs):
        # Allow user ID to be passed in the request and validate in the serializer
        return super().create(request, *args, **kwargs)

class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        # Order articles by 'created_at' field in descending order
        return Article.objects.all().order_by('-date')

class SingleArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  #increment views count
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
class ToggleLikeView(APIView):
    def post(self, request, format=None):
        serializer = ToggleLikeSerializer(data=request.data)
        
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            article_id = serializer.validated_data['article_id']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User with this ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

            article_like, created = ArticleLike.objects.get_or_create(user=user, article=article)

            if not created:
                # If the like already exists, the user is "disliking" the article (remove the like)
                article.likes -= 1
                article.likes = max(0, article.likes)  # Ensure likes don't go below 0
                article.save()

                # Remove the like entry from ArticleLike table
                article_like.delete()
                status_message = 'article disliked'
            else:
                # If no like exists, the user is "liking" the article
                article.likes += 1
                article.save()
                status_message = 'article liked'

            # Get the list of users who liked the article
            users_who_liked = User.objects.filter(articlelike__article=article)
            user_serializer = UserSerializer(users_who_liked, many=True)

            return Response({
                'status': status_message,
                'likes': article.likes,
                'users': user_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
class CreateCommentAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class SingleCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommunityStarView(APIView):
    def get(self, request, community_id):
        try:
            community = Community.objects.get(id=community_id)
        except Community.DoesNotExist:
            return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

        top_members = User.objects.filter(post__community=community)\
                                  .annotate(post_count=Count('post'))\
                                  .order_by('-post_count')[:3]

        result = []
        for member in top_members:
            result.append({
                'member_id': member.id,
                'member_name': member.email,
                'post_count': member.post_count
            })

        return Response(result, status=status.HTTP_200_OK)



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

class CommunityUpdate(generics.UpdateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

# Delete a community
class CommunityDelete(generics.DestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class JoinCommunityView(APIView):
    def post(self, request, community_id, format=None):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JoinCommunitySerializer(data={'community_id': community_id})
        if serializer.is_valid():
            try:
                community = serializer.join_community(user)
            except serializers.ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('author')  # Get the author ID from request data

        if not user_id:
            raise ValidationError({"detail": "User ID is required to create a post."})

        # Fetch the user based on the user_id
        user = get_object_or_404(User, id=user_id)

        # Save the post with the authenticated user as the author
        serializer.save(author=user)

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
        assignment_id = request.data.get('assignment_id')
        course_id = request.data.get('course_id')  # Ensure course_id is also handled

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = assignment.course  # Assume course is related to assignment
            if course.id != course_id:
                return Response({"error": "Course ID does not match assignment's course"}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({"error": "Assignment does not have a related course"}, status=status.HTTP_400_BAD_REQUEST)

        # Pass the user, assignment, and course to the serializer context
        serializer = self.get_serializer(data=request.data, context={'user_id': user.id, 'assignment_id': assignment.id, 'course_id': course.id, 'view': self})
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

class InstitutionList(APIView):
    def get(self, request):
        institutions = Institution.objects.all()
        # Pass the request context to the serializer
        serializer = InstitutionSerializer(institutions, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = InstitutionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete an institution by id
class InstitutionDetail(APIView):
    def get_object(self, pk):
        try:
            return Institution.objects.get(pk=pk)
        except Institution.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        institution = self.get_object(pk)
        # Pass the request context to the serializer
        serializer = InstitutionSerializer(institution, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        institution = self.get_object(pk)
        serializer = InstitutionSerializer(institution, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        institution = self.get_object(pk)
        institution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# Delete view to delete a project
class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDownloadView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404("Project not found.")
        
        # Increment total_downloads
        project.total_downloads += 1
        project.save()
        
        # Serve the file
        file_path = project.file.path  # Assuming 'file' is a FileField in Project model
        
        try:
            response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{project.file.name}"'
            return response
        except FileNotFoundError:
            raise Http404("File not found.")
        
        
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
    

from rest_framework.permissions import IsAuthenticated

class WaitingEventsView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.waiting()  # Fetch waiting events dynamically


class LiveEventsView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.live()  # Fetch live events dynamically


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

    def get_serializer_context(self):
        # Add the request to the serializer context
        return {'request': self.request}

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer  # Optional: To restrict access to authenticated users only
    lookup_field = 'id' 
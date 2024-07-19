# views.py
from turtle import pd
import logging

from accounts.models import User
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics,status
from .models import (Article, Comment,Category, Community, Enrollment, Post, Reply,Video,Project,
                     Assignment, Chapter, Choice, Course, Lecture, Question, Quiz, Submission,
                     Quiz, Question, Choice)
from .serializers import (ArticleSerializer, CategorySerializer, CommentSerializer, 
                          CommunitySerializer, EnrollmentSerializer, JoinCommunitySerializer, PostSerializer, ReplySerializer, ProjectSerializer,
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
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class SingleArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # Increment views count
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

class JoinCommunityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = JoinCommunitySerializer(data={'community_id': pk})
        if serializer.is_valid():
            community_id = serializer.validated_data['community_id']
            try:
                community = Community.objects.get(pk=community_id)
            except Community.DoesNotExist:
                return Response({'detail': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

            user = request.user
            if user in community.members.all():
                return Response({'detail': 'You are already a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)
            
            community.members.add(user)
            return Response({'detail': 'Joined community successfully.'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    queryset = Course.objects.filter(is_approved=True)
    serializer_class = CourseSerializer

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

class SubmissionListAPIView(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SubmissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


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
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        user = self.request.user

        # Check if the course exists
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already enrolled
        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({"error": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the enrollment
        enrollment = Enrollment.objects.create(user=user, course=course)
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EnrollmentListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)


class TakeCourseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        user = request.user

        if course.course_type == 'mooc':
            if Enrollment.objects.filter(user=user, course=course).exists():
                return Response({'detail': 'You are already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
            enrollment = Enrollment.objects.create(user=user, course=course)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'detail': 'Cannot self-enroll in SPOC courses.'}, status=status.HTTP_403_FORBIDDEN)

class AssignUsersToSPOCAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        if course.teacher != request.user:
            return Response({'detail': 'Only the course creator can assign users to this course.'}, status=status.HTTP_403_FORBIDDEN)
        emails = request.data.get('emails', [])
        assigned_users = []
        for email in emails:
            try:
                user = User.objects.get(email=email)
                if not Enrollment.objects.filter(user=user, course=course).exists():
                    enrollment = Enrollment.objects.create(user=user, course=course)
                    assigned_users.append(user.email)
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                # Maybe create a placeholder enrollment or send an invitation
                pass
        return Response({'assigned_users': assigned_users}, status=status.HTTP_201_CREATED)
    
class UploadExcelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        if course.teacher != request.user:
            return Response({'detail': 'Only the course creator can assign users to this course.'}, status=status.HTTP_403_FORBIDDEN)
        
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(file)
            emails = df['Email'].tolist()
            return self.assign_users_to_course(emails, course)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def assign_users_to_course(self, emails, course):
        assigned_users = []
        for email in emails:
            try:
                user = User.objects.get(email=email)
                if not Enrollment.objects.filter(user=user, course=course).exists():
                    enrollment = Enrollment.objects.create(user=user, course=course)
                    assigned_users.append(user.email)
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                # Maybe create a placeholder enrollment or send an invitation
                pass
        return Response({'assigned_users': assigned_users}, status=status.HTTP_201_CREATED)
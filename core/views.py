# views.py

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Article, Comment,Category, Community, Post, Reply,Video
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer, CommunitySerializer, PostSerializer, ReplySerializer, VideoSerializer

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



from rest_framework import generics
from .models import Assignment, Chapter, Choice, Course, Lecture, Question, Quiz, Submission
from .serializers import (AssignmentSerializer, ChapterSerializer, ChoiceSerializer, CourseSerializer,
LectureSerializer, QuestionSerializer, QuizSerializer, SubmissionSerializer)
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer, QuestionSerializer
##coursea
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

###chapters
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



# class QuizAPIView(APIView):
#     def get(self, request, quiz_id):
#         quiz = get_object_or_404(Quiz, id=quiz_id)
#         serializer = QuizSerializer(quiz)
#         return Response(serializer.data)

# class QuestionAPIView(APIView):
#     def get(self, request, question_id):
#         question = get_object_or_404(Question, id=question_id)
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     def post(self, request, question_id):
#         question = get_object_or_404(Question, id=question_id)
#         choice_id = request.data.get('choice_id')
#         if choice_id is None:
#             return Response({'error': 'No choice_id provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         choice = get_object_or_404(Choice, id=choice_id)
#         if choice.question != question:
#             return Response({'error': 'Choice does not belong to this question'}, status=status.HTTP_400_BAD_REQUEST)

#         is_correct = choice.is_correct
#         return Response({'is_correct': is_correct})



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



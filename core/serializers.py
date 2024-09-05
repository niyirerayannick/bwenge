from rest_framework import serializers
from accounts.models import User
from rest_framework.exceptions import ValidationError
from .models import (Article, ArticleLike, Comment, Category, Enrollment, Institution, UserAnswer, Video, Community, CommunityCategory, Post, Reply, 
Assignment, Choice, Course, Chapter, Lecture, Question, Quiz, Submission, Project)
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'comment', 'reply', 'date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'poster_image', 'description', 'categories', 'likes', 'views', 'author', 'date', 'comments']

    def create(self, validated_data):
        request = self.context.get('request')
        categories_data = validated_data.pop('categories', [])
        
        # Ensure that the author is set to the current user
        article = Article.objects.create(author=request.user, **validated_data)
        
        article.categories.set(categories_data)
        return article

class CommunityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityCategory
        fields = ['id', 'name']



class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'logo', 'email']

    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)
        
        # Get the request object to build the full URL
        request = self.context.get('request')
        if request:
            logo_url = instance.logo.url  # Get the relative URL of the logo
            full_logo_url = request.build_absolute_uri(logo_url)  # Build the full URL
            representation['logo'] = full_logo_url  # Update the logo field with the full URL
        
        return representation

class ProjectSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)  # Accept user_id in requests
    author = UserSerializer(read_only=True)  # Assuming author is a ForeignKey
    institution = serializers.PrimaryKeyRelatedField(
        queryset=Institution.objects.all()
    )  # Allow users to select an institution

    class Meta:
        model = Project
        fields = [
            'id', 'topics', 'description', 'tags', 'file', 'author', 'institution',
            'level', 'submitted_date', 'total_downloads', 'views', 'user_id',
        ]
        read_only_fields = ('total_downloads', 'views', 'submitted_date')  # Make certain fields read-only

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        
        if user_id is None:
            raise ValidationError('User ID must be provided.')
        
        try:
            author = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError('Invalid User ID provided.')

        institution = validated_data.pop('institution', None)
        project = Project.objects.create(author=author, institution=institution, **validated_data)
        return project

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class CommunitySerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=CommunityCategory.objects.all(), many=True
    )  # Specify many=True to handle multiple categories
    members = UserSerializer(many=True, read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'poster_image', 'admin', 'created_date', 'categories', 'members']

    def create(self, validated_data):
        # Extract and remove the categories field from validated_data
        categories_data = validated_data.pop('categories', [])
        community = Community.objects.create(**validated_data)
        
        # Add categories to the newly created community
        community.categories.set(categories_data)  # Use .set() to set multiple categories
        
        return community

    def update(self, instance, validated_data):
        # Extract and remove the categories field from validated_data
        categories_data = validated_data.pop('categories', None)
        
        # Update other fields using the parent class's update method
        instance = super().update(instance, validated_data)
        
        # Update the categories if provided
        if categories_data is not None:
            instance.categories.set(categories_data)  # Use .set() to replace the categories
        
        return instance

class JoinCommunitySerializer(serializers.Serializer):
    community_id = serializers.IntegerField()

    def validate_community_id(self, value):
        if not Community.objects.filter(id=value).exists():
            raise ValidationError("Community not found.")
        return value

    def join_community(self, user):
        community_id = self.validated_data['community_id']
        community = Community.objects.get(id=community_id)
        
        # Check if user is already a member
        if community.members.filter(id=user.id).exists():
            raise ValidationError("User is already a member of this community.")
        
        community.members.add(user)
        return community
    
class VideoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'poster_image', 'video_file', 'description', 'likes', 'categories', 'views', 'author', 'date', 'comments']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        video = Video.objects.create(**validated_data)
        video.categories.set(categories_data)
        return video

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content_type', 'text_content', 'file_content',
            'video_content', 'url_content', 'author', 'community'
        ]
        read_only_fields = ('created_at', 'likes', 'views')

    def get_author(self, obj):
        return [UserSerializer(obj.author).data]
    


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'video_url','video_file','pdf_url']

class ChapterSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'lectures']

class EnrollmentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['user_id', 'user_email', 'user_name']

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    course_type = serializers.CharField(source='get_course_type_display', read_only=True)
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    is_approved_status = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'course_image', 'chapters', 'teacher', 'is_approved', 'course_type', 'enrollments', 'is_approved_status']

    def create(self, validated_data):
        course_type = self.initial_data.get('course_type', 'mooc')
        validated_data['course_type'] = course_type
        return super().create(validated_data)
    
    def get_is_approved_status(self, obj):
        return "Awaiting approval" if not obj.is_approved else "Approved"

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)  # Nested CourseSerializer
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions','course']

class UserAnswerSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    selected_choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

class TakeQuizSerializer(serializers.Serializer):
    answers = UserAnswerSerializer(many=True)

    def validate(self, data):
        answers = data['answers']
        quiz = self.context['quiz']

        question_ids = set(quiz.questions.values_list('id', flat=True))
        for answer in answers:
            question_id = answer['question'].id
            if question_id not in question_ids:
                raise serializers.ValidationError("Invalid question in answers.")

        return data

    def create(self, validated_data):
        quiz = self.context['quiz']
        user = self.context['user']
        answers = validated_data['answers']

        correct_count = 0
        total_questions = len(answers)

        for answer in answers:
            question = answer['question']
            selected_choice = answer['selected_choice']
            is_correct = selected_choice.is_correct

            user_answer, created = UserAnswer.objects.update_or_create(
                user=user,
                question=question,
                defaults={
                    'selected_choice': selected_choice,
                    'is_correct': is_correct
                }
            )

            if is_correct:
                correct_count += 1

        score = (correct_count / total_questions) * 100

        return {
            'quiz_id': quiz.id,
            'score': score,
            'total_questions': total_questions,
            'correct_answers': correct_count
        }
    

class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    submissions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'course', 'submissions']

# SubmissionSerializer to serialize submission details
class SubmissionSerializer(serializers.ModelSerializer):
    # Include related user, assignment, and course information
    user_id = serializers.IntegerField(source='student.id', read_only=True)
    user_email = serializers.EmailField(source='student.email', read_only=True)
    user_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_id = serializers.IntegerField(source='assignment.id', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    course_id = serializers.IntegerField(source='assignment.course.id', read_only=True)
    course_title = serializers.CharField(source='assignment.course.title', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user_id', 'user_email', 'user_name', 'assignment_id', 'assignment_title', 'course_id', 'course_title', 'file', 'submitted_at']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        assignment_id = self.context.get('assignment_id')
        course_id = self.context.get('course_id')

        if not user_id:
            raise serializers.ValidationError("User ID must be provided to make a submission.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            raise serializers.ValidationError("Assignment not found.")
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course not found.")

        submission = Submission.objects.create(
            student=user,
            assignment=assignment,
            file=validated_data.get('file')
        )
        return submission
class UploadExcelSerializer(serializers.Serializer):
    file = serializers.FileField()

class EmailAssignmentSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False
    )

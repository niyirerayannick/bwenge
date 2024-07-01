from rest_framework import serializers
from accounts.models import User
from .models import (Article, Comment, Category, Institution, Video,Community, CommunityCategory,Post, Reply, 
Assignment, Choice, Course, Chapter, Lecture, Question, Quiz, Submission, Project)
from django.contrib.auth import get_user_model 
User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'topics', 'description', 'tags', 'file', 'author', 'level', 'submitted_date', 'total_downloads', 'views']

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

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
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=True)
   

    class Meta:
        model = Article
        fields = ['id', 'title', 'poster_image', 'description', 'categories', 'likes', 'views', 'author', 'date', 'comments']
        

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', None)
        article = Article.objects.create(**validated_data)
        if categories_data:
            for category in categories_data:
                article.categories.add(category)
        return article

class CommunitySerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=CommunityCategory.objects.all(), many=True, required=False)

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'poster_image', 'admin', 'created_date', 'categories']

    def create(self, validated_data):
        request = self.context.get('request')
        categories_data = validated_data.pop('categories', [])
        community = Community.objects.create(**validated_data)
        community.categories.set(categories_data)
        return community

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        
        instance = super().update(instance, validated_data)
        
        if categories_data is not None:
            instance.categories.set(categories_data)

        return instance
       

class VideoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Video
        fields = ['id', 'title', 'poster_image','video_file', 'description', 'likes', 'categories', 'views', 'author', 'date','comments']
        

    def create(self, validated_data):
        video_data = validated_data.pop('vides', None)
        video = Video.objects.create(**validated_data)
        if video_data:
            for video in video_data:
                video.categories.add(video)
        return video

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'video_url', 'pdf_url']

class ChapterSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'lectures']

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    course_type = serializers.CharField(source='get_course_type_display', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'course_image', 'chapters', 'teacher', 'is_approved', 'course_type']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to create a course.")

        # Ensure course_type is set, defaulting to 'mooc'
        course_type = self.initial_data.get('course_type', 'mooc')
        
        # Set teacher to the logged-in user
        validated_data['teacher'] = user
        validated_data['course_type'] = course_type
        return super().create(validated_data)
    
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
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'file', 'submitted_at']

class AssignmentSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'submissions']
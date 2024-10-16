# models.py
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
import pytz
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    poster_image = models.ImageField(upload_to='media/posters/')
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ArticleLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

class Video(models.Model):
    # VIDEO_FORMATS = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm']  # Add more video formats as needed

    # def validate_video_file_extension(value):
    #     if not value.name.split('.')[-1] in Video.VIDEO_FORMATS:
    #         raise ValidationError(f'Unsupported file format. Please upload a file with one of the following extensions: {", ".join(Video.VIDEO_FORMATS)}')

    # video_file = models.FileField(upload_to='media/videos/', validators=[validate_video_file_extension])
    # 
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster_image = models.ImageField(upload_to='media/video/posters/')
    youtube_link = models.URLField()
    categories = models.ManyToManyField(Category)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.comment

class CommunityCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    poster_image = models.ImageField(upload_to='media/posters/')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_communities')
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(CommunityCategory, related_name='communities')
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    FILE = 'file'
    VIDEO = 'video'
    URL = 'url'
    CONTENT_CHOICES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (FILE, 'File'),
        (VIDEO, 'Video'),
        (URL, 'URL'),
    ]

    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_CHOICES, default=TEXT)
    text_content = models.TextField(blank=True, null=True)
    file_content = models.FileField(upload_to='post_files/', blank=True, null=True)
    image_content = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video_content = models.FileField(upload_to='post_videos/', blank=True, null=True)
    url_content = models.URLField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    community = models.ForeignKey(Community, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Reply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.email} on post '{self.post.title}'"


class Institution(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='institution_logos/')
    email = models.EmailField(null=True, blank=True)  # Optional email field

    def __str__(self):
        return self.name

class Project(models.Model):
    BACHELOR = 'Bachelor'
    MASTERS = 'Masters'
    PHD = 'PhD'
    LEVEL_CHOICES = [
        (BACHELOR, 'Bachelor Degree'),
        (MASTERS, 'Master\'s Degree'),
        (PHD, 'PhD'),
    ]

    topics = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of tags")
    file = models.FileField(upload_to='project_files/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    submitted_date = models.DateTimeField(auto_now_add=True)
    total_downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    institution = models.ForeignKey('Institution', null=True, blank=True, on_delete=models.SET_NULL)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.topics

    def get_tags(self):
        return [tag.strip() for tag in self.tags.split(',') if tag]

    def set_tags(self, tags):
        self.tags = ','.join(tags)
        
class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('mooc', 'Mooc'), #mooc
        ('spoc', 'SPOC'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    course_image = models.ImageField(upload_to='media/course/posters/')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='mooc')

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, related_name='lectures', on_delete=models.CASCADE)
    video_url = models.URLField()
    video_file = models.FileField(upload_to='videos/')
    pdf_url = models.FileField(upload_to='media/COURSE/',)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.student

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} enrolled in {self.course.title}"
    
class PendingEnrollment(models.Model):
    email = models.EmailField()
    course = models.ForeignKey(Course, related_name='pending_enrollments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending enrollment for {self.email} in {self.course.title}"

class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'question')

# class EventManager(models.Manager):
#     def waiting(self):
#         return self.filter(event_time__gt=timezone.now(), approved=True)

#     def live(self):
#         now = timezone.now()
#         return self.filter(event_time__lte=now, event_time__gte=now - timezone.timedelta(hours=1), approved=True)
class EventManager(models.Manager):
    def waiting(self, user_timezone=None):
        now = timezone.now()
        if user_timezone:
            now = now.astimezone(pytz.timezone(user_timezone))
        return self.filter(event_time__gt=now, approved=True)

    def live(self, user_timezone=None):
        now = timezone.now()
        if user_timezone:
            now = now.astimezone(pytz.timezone(user_timezone))
        return self.filter(
            event_time__lte=now,
            event_time__gte=now - timezone.timedelta(hours=1),
            approved=True
        )
    
class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    flyer = models.ImageField(upload_to='flyers/')
    link = models.URLField()
    event_time = models.DateTimeField()
    approved = models.BooleanField(default=True)

    objects = EventManager()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Ensure event_time is timezone-aware
        if self.event_time and timezone.is_naive(self.event_time):
            self.event_time = timezone.make_aware(self.event_time, timezone.get_current_timezone())
        super().save(*args, **kwargs)

    def get_event_time_in_timezone(self, user_timezone):
        # Convert event_time to user's timezone for display purposes
        if user_timezone:
            return self.event_time.astimezone(pytz.timezone(user_timezone))
        return self.event_time  # Return in UTC if no timezone is provided
# models.py

from django.conf import settings
from django.db import models
from django.forms import ValidationError


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

    def __str__(self):
        return self.title

class Video(models.Model):
    VIDEO_FORMATS = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm']  # Add more video formats as needed

    def validate_video_file_extension(value):
        if not value.name.split('.')[-1] in Video.VIDEO_FORMATS:
            raise ValidationError(f'Unsupported file format. Please upload a file with one of the following extensions: {", ".join(Video.VIDEO_FORMATS)}')

    video_file = models.FileField(upload_to='media/videos/', validators=[validate_video_file_extension])
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster_image = models.ImageField(upload_to='media/video/posters/')
    categories = models.ManyToManyField(Category)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='video_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    reply = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

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
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='administered_communities', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_communities')
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(CommunityCategory, related_name='communities')

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
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='institution_members')

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
    tags = models.CharField(max_length=100)  # Assuming it's a comma-separated list of keywords
    file = models.FileField(upload_to='project_files/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    submitted_date = models.DateTimeField(auto_now_add=True)
    total_downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    institution = models.CharField(max_length=100)

    def __str__(self):
        return self.topics


from rest_framework import serializers
from .models import Article, Comment, Category, Video,Community, Post, Reply

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
    
    

class VideoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'description', 'likes', 'categories', 'views', 'author', 'date','comments']

    def create(self, validated_data):
        video_data = validated_data.pop('vides', None)
        video = Video.objects.create(**validated_data)
        if video_data:
            for video in video_data:
                video.categories.add(video)
        return video
    

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

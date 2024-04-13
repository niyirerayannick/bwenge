from django.contrib import admin
from .models import Article, Category, Comment, Community, Video, CommunityCategory

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(Community)
admin.site.register(CommunityCategory)




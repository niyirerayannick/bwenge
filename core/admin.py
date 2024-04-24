from django.contrib import admin
from .models import (Article, Category, Comment, Community, 
                     Video, CommunityCategory,Course, 
                     Chapter, Lecture, Quiz, Question,
                       Choice, Assignment, Submission)

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(Community)
admin.site.register(CommunityCategory)

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Assignment)
admin.site.register(Submission)




from django.contrib import admin
from .models import Course, Chapter, Lecture, Quiz, Question, Choice, Assignment, Submission

# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Assignment)
admin.site.register(Submission)

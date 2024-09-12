from django.contrib import admin

from .models import (
    Category, Article, Video, Comment, CommunityCategory, Community, Post, Reply,
    Institution, Project, Course, Chapter, Lecture, Quiz, Question, Choice,
    Assignment, Submission, Enrollment, PendingEnrollment, UserAnswer,Event
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'is_approved')
    search_fields = ('title', 'author__email')
    list_filter = ('is_approved', 'date')
    filter_horizontal = ('categories',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'is_approved')
    search_fields = ('title', 'author__email')
    list_filter = ('is_approved', 'date')
    filter_horizontal = ('categories',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'date', 'is_approved')
    search_fields = ('author__email', 'article__title', )
    list_filter = ('is_approved', 'date')

@admin.register(CommunityCategory)
class CommunityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'created_date', 'is_approved')
    search_fields = ('name', 'admin__email')
    list_filter = ('is_approved', 'created_date')
    filter_horizontal = ('categories', 'members')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'community', 'created_at', 'views', 'likes')
    search_fields = ('title', 'author__email', 'community__name')
    list_filter = ('created_at', 'content_type')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'created_at')
    search_fields = ('author__email', 'post__title')
    list_filter = ('created_at',)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('topics', 'author', 'level', 'submitted_date', 'total_downloads', 'views', 'is_approved')
    search_fields = ('topics', 'author__email')
    list_filter = ('level', 'submitted_date', 'is_approved')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'course_type', 'is_approved')
    search_fields = ('title', 'teacher__email')
    list_filter = ('course_type', 'is_approved')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter')
    search_fields = ('title', 'chapter__title')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text', 'quiz__title')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    search_fields = ('title', 'course__title')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at')
    search_fields = ('assignment__title', 'student__email')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    search_fields = ('user__email', 'course__title')

@admin.register(PendingEnrollment)
class PendingEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('email', 'course', 'created_at')
    search_fields = ('email', 'course__title')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_choice', 'is_correct')
    search_fields = ('user__email', 'question__text', 'selected_choice__text')
    list_filter = ('is_correct',)

class CustomDashboardAdmin(admin.ModelAdmin):
    change_list_template = 'admin/custom_dashboard.html'  # You can customize this template for more complex dashboards

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'event_time', 'user', 'approved')
    list_filter = ('event_time', 'approved')
    search_fields = ('title', 'description')
    readonly_fields = ('approved',)  # Make 'approved' field read-only

    def has_change_permission(self, request, obj=None):
        """
        Limit edit permissions: non-admin users cannot change the approval status.
        """
        if obj and not request.user.is_staff:
            if 'approved' in request.POST:
                return False
        return super().has_change_permission(request, obj)

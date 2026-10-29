from django.contrib import admin
from .models import Announcement, Assignment, Course, Enrollment, Lesson, Profile, Submission

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "category", "level", "is_published", "created_at")
    list_filter = ("is_published", "category", "level")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "max_score", "due_date")
    search_fields = ("title",)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "score", "submitted_at")
    list_filter = ("score",)
    search_fields = ("student__username", "assignment__title")
    fields = ("assignment", "student", "answer", "score", "feedback", "submitted_at")
    readonly_fields = ("submitted_at",)

admin.site.register(Profile)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Announcement)
admin.site.site_header = "Академія · керування навчанням"
admin.site.site_title = "Академія Admin"
admin.site.index_title = "Керування платформою"

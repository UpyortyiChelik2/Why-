from django.conf import settings
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = "student", "Студент"
        TEACHER = "teacher", "Викладач"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.STUDENT)
    bio = models.CharField(max_length=240, blank=True)
    def __str__(self):
        return f"{self.user.username} · {self.get_role_display()}"

class Course(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=80, default="Програмування")
    level = models.CharField(max_length=40, default="Початковий")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses_taught")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("course_detail", args=[self.pk])

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    video_url = models.URLField(blank=True)
    class Meta:
        ordering = ["order"]
        unique_together = [("course", "order")]
    def __str__(self):
        return f"{self.course.title}: {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["student", "course"], name="unique_course_enrollment")]
    def __str__(self):
        return f"{self.student} → {self.course}"

class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=180)
    description = models.TextField()
    max_score = models.PositiveIntegerField(default=100)
    due_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["assignment", "student"], name="unique_assignment_submission")]
    def __str__(self):
        return f"{self.student}: {self.assignment}"

class Announcement(models.Model):
    title = models.CharField(max_length=180)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title

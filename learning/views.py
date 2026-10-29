from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, SubmissionForm
from .models import Announcement, Assignment, Course, Enrollment, Lesson, Submission

def home(request):
    courses = Course.objects.filter(is_published=True).select_related("teacher")[:3]
    announcements = Announcement.objects.filter(is_active=True)[:3]
    return render(request, "learning/home.html", {"courses": courses, "announcements": announcements})

def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related("teacher")
    query = request.GET.get("q", "").strip()
    if query:
        courses = courses.filter(title__icontains=query) | courses.filter(description__icontains=query)
    category = request.GET.get("category", "").strip()
    if category:
        courses = courses.filter(category__iexact=category)
    return render(request, "learning/course_list.html", {"courses": courses.distinct(), "query": query})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, is_published=True)
    enrolled = request.user.is_authenticated and Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, "learning/course_detail.html", {"course": course, "enrolled": enrolled})

@login_required
@require_POST
def enroll(request, pk):
    course = get_object_or_404(Course, pk=pk, is_published=True)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, "Ви успішно записалися на курс.")
    return redirect("course_detail", pk=pk)

@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson.objects.select_related("course"), pk=pk)
    allowed = request.user.is_staff or lesson.course.teacher_id == request.user.id or Enrollment.objects.filter(student=request.user, course=lesson.course).exists()
    if not allowed:
        messages.error(request, "Спочатку запишіться на курс, щоб відкрити урок.")
        return redirect("course_detail", pk=lesson.course_id)
    return render(request, "learning/lesson_detail.html", {"lesson": lesson})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment.objects.select_related("lesson__course"), pk=pk)
    course = assignment.lesson.course
    allowed = request.user.is_staff or course.teacher_id == request.user.id or Enrollment.objects.filter(student=request.user, course=course).exists()
    if not allowed:
        messages.error(request, "Завдання доступне лише учасникам курсу.")
        return redirect("course_detail", pk=course.pk)
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    return render(request, "learning/assignment_detail.html", {"assignment": assignment, "submission": submission, "form": SubmissionForm(instance=submission)})

@login_required
@require_POST
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment.objects.select_related("lesson__course"), pk=pk)
    if not Enrollment.objects.filter(student=request.user, course=assignment.lesson.course).exists() and not request.user.is_staff:
        messages.error(request, "Ви не записані на цей курс.")
        return redirect("course_detail", pk=assignment.lesson.course_id)
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    form = SubmissionForm(request.POST, instance=submission)
    if form.is_valid():
        item = form.save(commit=False)
        item.assignment, item.student = assignment, request.user
        item.score = None
        item.save()
        messages.success(request, "Відповідь збережено.")
    else:
        messages.error(request, "Перевірте текст відповіді.")
    return redirect("assignment_detail", pk=pk)

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related("course")
    submissions = Submission.objects.filter(student=request.user).select_related("assignment", "assignment__lesson", "assignment__lesson__course").order_by("-submitted_at")[:8]
    return render(request, "learning/dashboard.html", {"enrollments": enrollments, "submissions": submissions})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Акаунт створено. Починайте навчання.")
        return redirect("dashboard")
    return render(request, "learning/auth_form.html", {"form": form, "title": "Створити акаунт", "button": "Зареєструватися"})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard")
    return render(request, "learning/auth_form.html", {"form": form, "title": "З поверненням", "button": "Увійти"})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("dashboard")

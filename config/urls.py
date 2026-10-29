from django.contrib import admin
from django.urls import path
from learning import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/<int:pk>/enroll/", views.enroll, name="enroll"),
    path("lessons/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("assignments/<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("assignments/<int:pk>/submit/", views.submit_assignment, name="submit_assignment"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
]

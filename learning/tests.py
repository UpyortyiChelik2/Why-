from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Course, Enrollment, Profile

class LearningFlowTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="test-pass-123")
        self.student = User.objects.create_user(username="student", password="test-pass-123")
        self.course = Course.objects.create(title="Python basics", slug="python-basics", description="Intro course", teacher=self.teacher)

    def test_course_catalog_is_public(self):
        response = self.client.get(reverse("course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python basics")

    def test_enrollment_requires_login(self):
        response = self.client.post(reverse("enroll", args=[self.course.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_student_can_enroll(self):
        self.client.login(username="student", password="test-pass-123")
        response = self.client.post(reverse("enroll", args=[self.course.pk]))
        self.assertRedirects(response, reverse("course_detail", args=[self.course.pk]))
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_profile_created_for_new_user(self):
        self.assertEqual(self.student.profile.role, Profile.Role.STUDENT)

from unittest import result

from django.urls import reverse
from rest_framework import status
from rest_framework.templatetags.rest_framework import data
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Test", description="...")
        self.lesson = Lesson.objects.create(lesson_name="Урок 1", lesson_description="Введение", course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("lesson_name"), self.lesson.lesson_name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "lesson_name": "Урок_2"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.filter(lesson_name="Урок_2").count(), 1
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "lesson_name": "Урок_2"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("lesson_name"), "Урок_2"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_list_lesson(self):
        course = Course.objects.create(
            name='Тестовый курс',
            description='Тест',
        )

        Lesson.objects.create(
            lesson_name='Тестовый урок',
            lesson_description='Тест',
            lesson_url=course,
            owner=self.user
        )

        response = self.client.get(
            '/materials/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Test", description="...", owner=self.user)
        self.lesson = Lesson.objects.create(lesson_name="Урок 1", lesson_description="Введение", course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {"name": "Математический анализ"}
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Линейная алгебра"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Линейная алгебра"
        )

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_list_course(self):
        response = self.client.get(
            '/materials/course/',
        )
        print(response)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'name': 'Test', 'description': '...', 'preview': None, 'owner': None, 'subscription': False,
                 'course_lessons': [
                     {'id': 4, 'name': 'Урок 1', 'description': 'Введение', 'preview': None, 'link': None, 'course': 5,
                      'owner': 4}
                 ],
                 'course_lesson_count': 1}
            ]}

        )
        self.assertEqual(response.status_code, status.HTTP_200_OK),
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="subtest@mail.ru")
        self.course = Course.objects.create(title="Подписка", description="Тест подписки", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_message = f'подписка на курс {self.course.title} добавлена'
        self.assertEqual(response.json(), {"message": expected_message})

    def test_unsubscribe(self):
        url = reverse("materials:subscription")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_message = f'подписка на курс {self.course.title} удалена'
        self.assertEqual(response.json(), {"message": expected_message})

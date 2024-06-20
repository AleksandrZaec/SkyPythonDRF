from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer


class LessonCRUDTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные: курс и уроки
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.lesson1 = Lesson.objects.create(title='Lesson 1', course=self.course, owner=self.user)
        self.lesson2 = Lesson.objects.create(title='Lesson 2', course=self.course, owner=self.user)

    def test_create_lesson(self):
        url = '/lesson/create/'
        data = {'title': 'New Lesson', 'description': 'Description of new lesson', 'course': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)  # Проверяем, что урок был создан

    def test_update_lesson(self):
        url = f'/lesson/{self.lesson1.id}/update/'
        data = {'title': 'Updated Lesson 1', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.title, 'Updated Lesson 1')

    def test_delete_lesson(self):
        url = f'/lesson/{self.lesson2.id}/destroy/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson2.id).exists())


class SubscriptionTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные: курс и подписка
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_create_subscription(self):
        url = '/subscription/'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Подписка удалена')  # Проверяем, что подписка была удалена, так как уже существовала

    def test_list_subscriptions(self):
        url = '/subscription/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что получили одну подписку

    def test_create_subscription_unauthenticated(self):
        # Проверяем, что невозможно создать подписку без аутентификации
        self.client.force_authenticate(user=None)
        url = '/subscription/'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

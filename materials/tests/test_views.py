from django.test import TestCase
from rest_framework.test import APIClient

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='1234')
        self.course = Course.objects.create(title='Глубокое погружение в Django', owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'title': 'Введение в ад',
            'description': 'Лекция о том, почему Django такой...',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_list_lessons(self):
        Lesson.objects.create(title='Лекция 1', course=self.course, owner=self.user)
        Lesson.objects.create(title='Лекция 2', course=self.course, owner=self.user)

        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(title='Старое имя', course=self.course, owner=self.user)
        response = self.client.patch(f'/api/lessons/{lesson.id}/', {'title': 'Новое имя'})
        self.assertEqual(response.status_code, 200)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Новое имя')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(title='Удаляемый', course=self.course, owner=self.user)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='1234')
        self.course = Course.objects.create(title='DRF для тех, кто уже плакал', owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        response = self.client.post('/api/subscribe/', {'course': self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_double_subscription(self):
        self.client.post('/api/subscribe/', {'course': self.course.id})
        response = self.client.post('/api/subscribe/', {'course': self.course.id})
        self.assertEqual(response.status_code, 400)

    def test_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete('/api/unsubscribe/', {'course': self.course.id})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_not_subscribed(self):
        response = self.client.delete('/api/unsubscribe/', {'course': self.course.id})
        self.assertEqual(response.status_code, 404)

    def test_is_subscribed_field(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_subscribed', response.data)
        self.assertTrue(response.data['is_subscribed'])

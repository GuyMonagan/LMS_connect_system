from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from materials.models import Course, Subscription
from materials.tasks import send_course_update_email
from unittest.mock import patch

User = get_user_model()


class SendCourseUpdateEmailTaskTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title="Test Course")
        self.user1 = User.objects.create_user(email="user1@example.com", password="test")
        self.user2 = User.objects.create_user(email="user2@example.com", password="test")

        # Подписываем пользователей на курс
        Subscription.objects.create(course=self.course, user=self.user1)
        Subscription.objects.create(course=self.course, user=self.user2)


    @patch("materials.tasks.send_mail")
    def test_email_sent_to_all_subscribers(self, mock_send_mail):
        """Убедимся, что письма отправляются всем подписчикам"""
        send_course_update_email(self.course.id)

        self.assertEqual(mock_send_mail.call_count, 2)

        # Проверим аргументы вызовов
        calls = mock_send_mail.call_args_list
        emails_sent = [call[1]['recipient_list'][0] for call in calls]
        self.assertIn(self.user1.email, emails_sent)
        self.assertIn(self.user2.email, emails_sent)


    @patch("materials.tasks.send_mail")
    def test_no_subscribers_no_email_sent(self, mock_send_mail):
        """Если подписчиков нет — письма не отправляются"""
        Subscription.objects.all().delete()

        send_course_update_email(self.course.id)

        mock_send_mail.assert_not_called()

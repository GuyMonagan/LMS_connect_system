from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from materials.tasks import deactivate_inactive_users


class DeactivateInactiveUsersTest(TestCase):
    def test_deactivates_users_who_didnt_login_30_days(self):
        # пользователь, который не заходил 40 дней назад
        old_user = User.objects.create_user(email='old@example.com', password='1234')
        old_user.last_login = timezone.now() - timedelta(days=40)
        old_user.save()

        # активный пользователь
        active_user = User.objects.create_user(email='active@example.com', password='1234')
        active_user.last_login = timezone.now()
        active_user.save()

        # запускаем таску (не через .delay(), а напрямую)
        deactivate_inactive_users()

        # обновим из базы
        old_user.refresh_from_db()
        active_user.refresh_from_db()

        self.assertFalse(old_user.is_active)  # должен быть заблокирован
        self.assertTrue(active_user.is_active)  # должен остаться активным

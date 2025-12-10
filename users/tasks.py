from celery import shared_task
from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=threshold)
    inactive_users.update(is_active=False)

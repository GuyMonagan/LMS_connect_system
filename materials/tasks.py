from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course).select_related('user')

    for sub in subscribers:
        user = sub.user
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Здравствуйте, {user.email}!\n\nКурс "{course.title}" был обновлён. Проверьте новые материалы на платформе.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,  # Теперь ошибки будут отображаться
        )


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=threshold)
    inactive_users.update(is_active=False)

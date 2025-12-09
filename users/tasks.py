from celery import shared_task
from django.core.mail import send_mail
from materials.models import Course, Subscription
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscriber_emails = Subscription.objects.filter(course=course).values_list('user__email', flat=True)

    for email in subscriber_emails:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Здравствуйте, {email}!\n\nКурс "{course.title}" был обновлён. Проверьте новые материалы на платформе.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=threshold)
    inactive_users.update(is_active=False)

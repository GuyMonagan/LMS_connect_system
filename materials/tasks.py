from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription


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

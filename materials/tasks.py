from datetime import timedelta
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.timezone import now
from users.models import User


@shared_task
def send_course_update_email(user_email, course_title):
    send_mail(
        'Course Updated',
        f'The course "{course_title}" has been updated.',
        'zaecaam95@mail.ru',
        [user_email],
        fail_silently=False,
    )


@shared_task
def block_inactive_users_task():
    User = get_user_model()
    threshold_date = now() - timedelta(days=30)  # Пользователи, не активные более 30 дней
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)

    for user in inactive_users:
        user.is_active = False

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from materials.models import Course, Lesson
from users.models import Payment
from datetime import date


class Command(BaseCommand):
    help = 'Load payments data'

    def handle(self, *args, **kwargs):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        course1 = Course.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=1)

        payments = [
            Payment(user=user1, payment_date=date(2024, 6, 1), paid_course=course1, paid_lesson=None, amount=100.00,
                    payment_method='cash'),
            Payment(user=user2, payment_date=date(2024, 6, 2), paid_course=None, paid_lesson=lesson1, amount=50.00,
                    payment_method='bank_transfer')
        ]

        Payment.objects.bulk_create(payments)

        self.stdout.write(self.style.SUCCESS('Successfully loaded payments data'))

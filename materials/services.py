from datetime import timedelta
from django.utils import timezone
from .models import Subscription
from .tasks import send_course_update_email


class CourseService:
    @staticmethod
    def notify_subscribers(course):
        now = timezone.now()
        if now - course.updated_at > timedelta(hours=4):
            subscriptions = Subscription.objects.filter(course=course)
            for subscription in subscriptions:
                send_course_update_email.delay(subscription.user.email, course.name)

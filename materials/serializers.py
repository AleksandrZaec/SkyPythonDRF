from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import YouTubeLinkValidator  # validate_youtube_link,


class LessonSerializer(ModelSerializer):
    # video_link = serializers.URLField(validators=[validate_youtube_link])

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkValidator(field='video_link')]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    number_of_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_number_of_lessons(self, course):
        return course.lesson_set.count()

    def get_is_subscribed(self, course):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=course).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_staff or instance.user == user:
                return super().to_representation(instance)
            return {}
        return super().to_representation(instance)

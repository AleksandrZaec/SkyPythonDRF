from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    number_of_lessons = SerializerMethodField()

    def get_number_of_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"

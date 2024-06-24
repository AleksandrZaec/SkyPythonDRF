from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404

from materials.paginators import MaterialsPaginator
from materials.permissions import IsModeratorOrReadOnly, IsOwnerOrModerator, IsOwnerOrReadOnly
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.models import Course, Lesson, Subscription


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    paginator_class = MaterialsPaginator

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class CourseViewSet(ModelViewSet):
#     queryset = Course.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return CourseDetailSerializer
#         return CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly]
    paginator_class = MaterialsPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly, IsOwnerOrReadOnly]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


post_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['course_id'],
    properties={
        'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the course')
    }
)

post_response_schema = openapi.Response(
    description='Subscription status message',
    examples={
        'application/json': {'message': 'Подписка добавлена'}
    }
)

# Схема для метода GET
get_response_schema = openapi.Response(
    description='List of subscriptions',
    schema=SubscriptionSerializer(many=True)
)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create or delete a subscription to a course.",
        request_body=post_request_schema,
        responses={200: post_response_schema}
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message})

    @swagger_auto_schema(
        operation_description="Retrieve the list of subscriptions for the authenticated user.",
        responses={200: get_response_schema}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            subscriptions = Subscription.objects.all()
        else:
            subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from materials.permissions import IsModeratorOrReadOnly, IsOwnerOrModerator, IsOwnerOrReadOnly
from materials.serializers import CourseSerializer, LessonSerializer
from materials.models import Course, Lesson


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
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

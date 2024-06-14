from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet)


urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name='Lesson_list'),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name='Lesson_retrieve'),
    path("lesson/create/", LessonCreateAPIView.as_view(), name='Lesson_create'),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name='Lesson_update'),
    path("lesson/<int:pk>/destroy/", LessonDestroyAPIView.as_view(), name='Lesson_destroy'),
]

urlpatterns += router.urls

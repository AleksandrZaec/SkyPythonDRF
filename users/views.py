from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer
from users.models import User


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListAPIViewAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
    Обновление профиля пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get_object(self):
        return self.request.user
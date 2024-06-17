from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from users.serializers import UserSerializer, PaymentSerializer
from users.models import User, Payment
from .filters import PaymentFilter
from .permissions import IsModeratorOrOwner


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner]


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner]


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
    Обновление профиля пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if self.get_object() != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['payment_date']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            # Модератор видит все платежи
            return Payment.objects.all()
        else:
            # Обычные пользователи видят только свои платежи
            return Payment.objects.filter(user=self.request.user)

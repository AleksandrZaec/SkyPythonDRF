import stripe
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.serializers import UserSerializer, PaymentSerializer
from users.models import User, Payment
from .filters import PaymentFilter
from .permissions import IsModeratorOrOwner
from .services import convert_rub_to_dollars, create_stripe_price, create_stripe_product, \
    create_stripe_session


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


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a payment and get a Stripe payment link.",
        responses={201: openapi.Response(
            description="Payment link",
            examples={'application/json': {'payment_link': 'https://stripe.com/payment_link'}}
        )}
    )
    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product_id = create_stripe_product(
            name=f"Payment for {payment.paid_course or payment.paid_lesson}",
            description="Course or Lesson Payment"
        )

        price_id = create_stripe_price(product_id, payment.amount)
        session_id, payment_link = create_stripe_session(price_id)

        # Обновление информации о платеже
        payment.stripe_session_id = session_id
        payment.link = payment_link
        payment.save()

        return Response({'payment_link': payment_link}, status=status.HTTP_201_CREATED)


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = stripe.checkout.Session.retrieve(session_id)
        return Response({'status': session.payment_status})

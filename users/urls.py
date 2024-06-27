from django.urls import path
from users.views import UserProfileUpdateAPIView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, UserDestroyAPIView, PaymentListView, PaymentCreateAPIView, PaymentStatusAPIView
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

app_name = UsersConfig.name


class CreatePaymentView:
    pass


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/destroy/', UserDestroyAPIView.as_view(), name='user_destroy'),
    path('profile/', UserProfileUpdateAPIView.as_view(), name='user_profile'),
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('create-payment/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('payment-status/<str:session_id>/', PaymentStatusAPIView.as_view(), name='payment-status')
]






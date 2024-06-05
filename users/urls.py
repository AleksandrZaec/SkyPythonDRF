from django.urls import path

from materials.apps import MaterialsConfig
from users.views import UserProfileUpdateAPIView, UserCreateAPIView, UserListAPIViewAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/', UserListAPIViewAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/destroy/', UserDestroyAPIView.as_view(), name='user_destroy'),
    path('user/profile/', UserProfileUpdateAPIView.as_view(), name='user_profile'),
]
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.seriallzers import UserSerializer
from users.permissions import IsOwnerUser


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для изменения пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerUser]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для просмотра пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Контреллер для удаления пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerUser]

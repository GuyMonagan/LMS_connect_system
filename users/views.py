from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .permissions import IsSelf
from .serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступна без авторизации.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    """
    Список пользователей.
    Доступен только авторизованным.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            # редактировать — только себя
            return [IsAuthenticated(), IsSelf()]

        # GET — любой авторизованный
        return [IsAuthenticated()]


class UserUpdateView(generics.RetrieveUpdateAPIView):
    """
    Для редактирования профиля был использован RetrieveUpdateAPIView,
    так как он проще, чище и логичнее в этом контексте, чем ViewSet —
    профиль редактирует только один пользователь и не требует полного CRUD.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

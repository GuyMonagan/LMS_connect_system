from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    """
    Для редактирования профиля был использован RetrieveUpdateAPIView,
    так как он проще, чище и логичнее в этом контексте, чем ViewSet —
    профиль редактирует только один пользователь и не требует полного CRUD.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

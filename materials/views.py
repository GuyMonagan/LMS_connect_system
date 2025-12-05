from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # запрещаем модераторам create + destroy
        if self.action in ('create', 'destroy'):
            permission_classes = [IsAuthenticated, ~IsModer]

        # update / partial_update — модератор ИЛИ владелец
        elif self.action in ('update', 'partial_update'):
            permission_classes = [IsAuthenticated, IsModer | IsOwner]

        # retrieve / list — любой авторизованный
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # автоматическая привязка владельца
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]

        elif self.request.method == 'POST':
            # модератор НЕ может создавать
            permission_classes = [IsAuthenticated, ~IsModer]

        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            # редактировать может модератор или владелец
            permission_classes = [IsAuthenticated, IsModer | IsOwner]

        elif self.request.method == 'DELETE':
            # модератор НЕ может удалять, только владелец
            permission_classes = [IsAuthenticated, IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]

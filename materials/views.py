from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.tasks import send_course_update_email
from users.permissions import IsModer, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import CustomPagination
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


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


    def perform_update(self, serializer):
        instance = serializer.save()
        send_course_update_email.delay(instance.id)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

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


class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course')
        course = Course.objects.get(id=course_id)
        sub, created = Subscription.objects.get_or_create(user=request.user, course=course)
        if not created:
            return Response({'detail': 'Вы уже подписаны на этот курс.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Подписка успешно создана.'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        course_id = request.data.get('course')
        try:
            sub = Subscription.objects.get(user=request.user, course_id=course_id)
            sub.delete()
            return Response({'detail': 'Подписка удалена.'}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({'detail': 'Подписка не найдена.'}, status=status.HTTP_404_NOT_FOUND)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from .views import SubscribeView

app_name = 'materials'


router = DefaultRouter()
router.register(r'courses', CourseViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
    path('subscribe/', SubscribeView.as_view()),
    path('unsubscribe/', SubscribeView.as_view()),
]

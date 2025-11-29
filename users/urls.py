from django.urls import path
from .views import (
    UserListCreateView,
    UserRetrieveUpdateDeleteView,
    UserUpdateView
)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),               # /api/users/
    path('<int:pk>/', UserRetrieveUpdateDeleteView.as_view(), name='user-detail'), # /api/users/1/
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user-update'),       # /api/users/profile/1/
]

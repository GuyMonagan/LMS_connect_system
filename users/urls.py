from django.urls import path

from .views import (
    UserListView,
    UserRegisterView,
    UserRetrieveUpdateDeleteView,
    UserUpdateView,
)

app_name = 'users'


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),     # POST
    path('', UserListView.as_view(), name='list'),                      # GET
    path('<int:pk>/', UserRetrieveUpdateDeleteView.as_view(), name='detail'),  # GET/PUT/PATCH/DELETE
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='profile'),       # GET/PATCH/PUT (потом ограничить по владельцу)
]

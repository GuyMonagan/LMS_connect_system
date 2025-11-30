from django.urls import path
from .views import PaymentListView  # пока только это

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
]

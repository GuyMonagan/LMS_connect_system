
from django.urls import path
from .views import PaymentListCreateView, PaymentStatusView

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list-create'),  # <--- и GET, и POST
    path('<int:pk>/status/', PaymentStatusView.as_view(), name='payment-status'),
]
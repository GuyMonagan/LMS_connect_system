from django.shortcuts import render
from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PaymentFilter
from rest_framework.permissions import IsAuthenticated


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # создаём продукт
        product_id = create_stripe_product(payment.course.title)

        # создаём цену
        price_id = create_stripe_price(product_id, payment.amount)

        # создаём сессию
        session_url = create_checkout_session(
            price_id,
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/"
        )

        # сохраняем ссылку
        payment.payment_url = session_url
        payment.save()

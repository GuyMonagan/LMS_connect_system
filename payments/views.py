from django.shortcuts import render
from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PaymentFilter
from rest_framework.permissions import IsAuthenticated
import stripe
import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # на всякий случай выберем заголовок: либо курс, либо урок
        title = None
        if payment.course:
            title = payment.course.title
        elif payment.lesson:
            title = payment.lesson.title
        else:
            title = "Оплата без курса"

        product_id = create_stripe_product(title)
        price_id = create_stripe_price(product_id, payment.amount)

        session = create_checkout_session(
            price_id,
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )

        payment.payment_url = session["url"]      # можно и session.url
        payment.stripe_session_id = session["id"]
        payment.save()


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Платёж не найден"}, status=404)

        if not payment.stripe_session_id:
            return Response({"error": "Нет Stripe session ID"}, status=400)

        # получаем данные о сессии
        session = stripe.checkout.Session.retrieve(payment.stripe_session_id)

        return Response({
            "payment_id": payment.id,
            "status": session.get("payment_status"),
            "stripe_status": session.get("status"),
            "amount_total": session.get("amount_total"),
        })

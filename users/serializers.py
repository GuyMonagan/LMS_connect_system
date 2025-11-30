from rest_framework import serializers
from .models import User
from payments.serializers import PaymentShortSerializer


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentShortSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']

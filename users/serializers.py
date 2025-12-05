from rest_framework import serializers
from .models import User
from payments.serializers import PaymentShortSerializer


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentShortSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']


    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = self.context['request'].user

        # если чужой профиль — скрываем поля
        if user.id != instance.id:
            data.pop('phone', None)
            data.pop('city', None)
            data.pop('payments', None)

        return data

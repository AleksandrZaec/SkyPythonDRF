from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'city', 'avatar', 'payments']

    def get_payments(self, obj):
        request = self.context.get('request')
        if request.user == obj or request.user.is_staff:
            return PaymentSerializer(obj.payment_set.all(), many=True).data
        else:
            return []

    def to_representation(self, instance):
        """
        Переопределяем метод to_representation для скрытия фамилии при просмотре профиля других пользователей.
        """
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user != instance and not request.user.is_staff:
            ret.pop('last_name', None)
        return ret

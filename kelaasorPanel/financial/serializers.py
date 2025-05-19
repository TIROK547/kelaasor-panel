from rest_framework.serializers import ModelSerializer
from .models import Payment, Factor

class FactorSerializer(ModelSerializer):
    """
    Serializer for the Factor model, representing a financial record for bootcamp registration.
    """
    class Meta:
        model = Factor
        fields = "__all__"
        

class PaymentSerializer(ModelSerializer):
    """
    Serializer for the Payment model, representing a payment towards a Factor.
    """
    class Meta:
        model = Payment
        fields = "__all__"

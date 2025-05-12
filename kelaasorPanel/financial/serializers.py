from rest_framework.serializers import ModelSerializer
from .models import Payment, Factor

class FactorSerializer(ModelSerializer):
    class Meta:
        model = Factor
        fields = "__all__"
        

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
    
        
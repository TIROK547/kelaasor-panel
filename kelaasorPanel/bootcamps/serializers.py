from rest_framework.serializers import ModelSerializer
from .models import BootCamp, InPersonBootCamp, OnlineBootCamp


class BootCampSerializer(ModelSerializer):
    class Meta:
        model = BootCamp
        fields = "__all__"
        
        
class InPersonBootCampSerializer(ModelSerializer):
    class Meta:
        model = InPersonBootCamp
        fields = "__all__"
    
    
class OnlineBootCampSerializer(ModelSerializer):
    class Meta:
        model = OnlineBootCamp
        fields = "__all__"
    
        
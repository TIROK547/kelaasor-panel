from rest_framework.serializers import ModelSerializer
from .models import BootCamp, BootCampCategory, BootCampsJoinRequest


class BootCampCategorySerializer(ModelSerializer):
    class Meta:
        model = BootCampCategory
        fields = "__all__"
        
        
class BootCampSerializer(ModelSerializer):
    class Meta:
        model = BootCamp
        fields = "__all__"
        
        
class BootCampsJoinRequestSerializer(ModelSerializer):
    class Meta:
        model = BootCampsJoinRequest
        fields = "__all__"
    
        
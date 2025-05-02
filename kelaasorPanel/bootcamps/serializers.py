from rest_framework.serializers import ModelSerializer
from .models import BootCamp, BootCampCategory


class BootCampCategorySerializer(ModelSerializer):
    class Meta:
        model = BootCampCategory
        fields = "__all__"
        
        
class BootCampSerializer(ModelSerializer):
    class Meta:
        model = BootCamp
        fields = "__all__"
    
        
from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"
        
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user
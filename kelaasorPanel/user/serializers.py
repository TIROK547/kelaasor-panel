from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    """
    Serializer for User model that handles password hashing on creation.
    """
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user



class CustomAccountSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]




class CAccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


from rest_framework.serializers import ModelSerializer
from .models import BootCamp, BootCampCategory, BootCampsJoinRequest
from rest_framework import serializers

class BootCampCategorySerializer(ModelSerializer):
    class Meta:
        model = BootCampCategory
        fields = "__all__"
        
        
class BootCampSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootCamp
        fields = '__all__'

    def create(self, validated_data):
        category = validated_data['category']
        bootcamp_type = validated_data['bootcamp_type']

        if bootcamp_type != category.bootcamp_type:
            raise serializers.ValidationError({
                'bootcamp_type': 'نوع بوت‌کمپ باید با نوع دسته‌بندی آن مطابقت داشته باشد.'
            })

        return super().create(validated_data)

        
class BootCampsJoinRequestSerializer(ModelSerializer):
    class Meta:
        model = BootCampsJoinRequest
        fields = "__all__"
        read_only_fields = ['user']
    
        
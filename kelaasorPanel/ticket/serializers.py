from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Ticket, Message
from user.models import User

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['user', 'date_created', 'status']
        

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['user', 'date_sended']


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status']

    def validate_status(self, value):
        allowed_statuses = ['pending', 'answered', 'unanswered', 'closed']
        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid status value.")
        return value
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Ticket, Message
from user.models import User
from django.utils import timezone
from datetime import timedelta

class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for Ticket model.
    
    Includes a computed 'status' field which indicates the current state of the ticket
    based on the last message's date and whether an admin has replied.
    """
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['user', 'date_created', 'status']
    
    def get_status(self, ticket):
        """
        Determines the status of the ticket based on message activity.
        
        Returns:
            str: One of "closed", "answered", "unanswered", "pending", or "no messages".
        """
        last_message = Message.objects.filter(ticket=ticket).order_by('-date_sended').first()
        has_admin_reply = Message.objects.filter(ticket=ticket, user__is_staff=True).exists()
        
        if last_message:
            if timezone.now() - last_message.date_sended > timedelta(days=7):
                return "closed"
            elif has_admin_reply:
                return "answered" if last_message.user.is_staff else "unanswered"
            else:
                return "pending"

        return "no messages"
        

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['user', 'date_sended']

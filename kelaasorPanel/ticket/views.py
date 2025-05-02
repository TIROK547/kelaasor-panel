from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .serializers import TicketSerializer, MessageSerializer
from .models import Message, Ticket
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUserType, IsTicketOwnerOrSupport
from .tasks import alert_support
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError

class CreateTicketView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    def perform_create(self, serializer):
        ticket = serializer.save(user=self.request.user)
        alert_support.delay(user_id=self.request.user.id, ticket_id=ticket.id, category=ticket.category)
    
    
class CreateMessageView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        ticket = serializer.validated_data.get('ticket')

        if ticket.status == "closed":
            raise ValidationError("Cannot send message to a closed ticket.")

        serializer.save(user=self.request.user)
        
    
class ListTicketView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Ticket.objects.all()
        elif user.groups.filter(name='fin_support').exists():
            return Ticket.objects.filter(category='financial')
        elif user.groups.filter(name='tech_support').exists():
            return Ticket.objects.filter(category='technical')
        else:
            return Ticket.objects.filter(user=user)
        
     
class TicketMessagesView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTicketOwnerOrSupport]
    serializer_class = MessageSerializer

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        return Message.objects.filter(ticket_id=ticket_id).order_by('date_sended')
    
    

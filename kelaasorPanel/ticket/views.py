from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .serializers import TicketSerializer, MessageSerializer
from .models import Message, Ticket
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUserType, IsTicketOwnerOrSupport
from .tasks import alert_support
from rest_framework.exceptions import ValidationError

class CreateTicketView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    
    def perform_create(self, serializer):
        # Save the ticket with the current user as owner
        ticket = serializer.save(user=self.request.user)
        # Send notification email to support via Celery task
        alert_support.delay(user_id=self.request.user.id, ticket_id=ticket.id, category=ticket.category)
    
    
class CreateMessageView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        # Get the related ticket
        ticket = serializer.validated_data.get('ticket')

        # Prevent sending messages to closed tickets
        if ticket.status == "closed":
            raise ValidationError("Cannot send message to a closed ticket.")

        # Save the message with the current user as sender
        serializer.save(user=self.request.user)
        
    
class ListTicketView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user

        # Superuser sees all tickets
        if user.is_superuser:
            return Ticket.objects.all()
        # Financial support group sees only financial tickets
        elif user.groups.filter(name='fin_support').exists():
            return Ticket.objects.filter(category='financial')
        # Technical support group sees only technical tickets
        elif user.groups.filter(name='tech_support').exists():
            return Ticket.objects.filter(category='technical')
        # Regular users see only their own tickets
        else:
            return Ticket.objects.filter(user=user)
        
     
class TicketMessagesView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTicketOwnerOrSupport]
    serializer_class = MessageSerializer

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        # Return all messages for the ticket ordered by send date
        return Message.objects.filter(ticket_id=ticket_id).order_by('date_sended')

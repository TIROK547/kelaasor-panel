from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .serializers import TicketSerializer, MessageSerializer, TicketStatusUpdateSerializer
from .models import Message, Ticket
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUserType, IsTicketOwnerOrSupport
from .tasks import alert_support
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status

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
        serializer.save(user=self.request.user)
        
    
class ListTicketView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUserType]
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
            return Ticket.objects.none()
        
        
class TicketMessagesView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTicketOwnerOrSupport]
    serializer_class = MessageSerializer

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        return Message.objects.filter(ticket_id=ticket_id).order_by('date_sended')
    
    
class TicketStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserType]

    def patch(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=http_status.HTTP_404_NOT_FOUND)

        requested_status = request.data.get("status")
        if requested_status != "closed":
            return Response(
                {"detail": "Only status 'closed' can be set manually."},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        serializer = TicketStatusUpdateSerializer(ticket, data={"status": "closed"}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Ticket closed successfully.", "ticket": serializer.data})
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
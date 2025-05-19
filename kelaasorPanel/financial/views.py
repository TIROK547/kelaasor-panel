from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import PaymentSerializer, FactorSerializer
from .models import Payment, Factor
from rest_framework.response import Response
from rest_framework import status as drf_status


class ListAllPaymentsView(ListAPIView):
    """
    Admin view to list all payment records.
    """
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    
    
class ListUnpaidPaymentsView(ListAPIView):
    """
    Admin view to list all payments that have not been accepted yet.
    """
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.exclude(state='accepted')
    
    
class CreatePaymentView(CreateAPIView):
    """
    Admin view to create a new payment record.
    """
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class ListAllFactorsView(ListAPIView):
    """
    Admin view to list all financial factors (invoices).
    """
    permission_classes = [IsAdminUser]
    serializer_class = FactorSerializer
    queryset = Factor.objects.all()
    
    
class ListUnpaidFactorsView(ListAPIView):
    """
    Admin view to list all unpaid factors (invoices).
    """
    permission_classes = [IsAdminUser]
    serializer_class = FactorSerializer
    queryset = Factor.objects.filter(paid=False)


class DecidePaymentStateView(UpdateAPIView):
    """
    Admin view to update the state of a payment. 
    If payment is accepted, triggers payment logic and possibly marks the factor as paid.
    """
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    
    def patch(self, request, *args, **kwargs):
        """
        Handle partial update to change payment state. If payment gets accepted, calls mark_as_paid().
        """
        instance = self.get_object()
        prev_status = instance.state
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_status = serializer.validated_data.get('state')
        
        if new_status == 'accepted' and prev_status != 'accepted':
            instance.mark_as_paid()
            return Response(serializer.data, status=drf_status.HTTP_200_OK)
        
        return Response(serializer.data, status=drf_status.HTTP_400_BAD_REQUEST)

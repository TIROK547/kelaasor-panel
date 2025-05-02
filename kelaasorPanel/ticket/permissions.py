from rest_framework.permissions import BasePermission

class IsAdminUserType(BasePermission):
    """
    Allows access only to financial admins, other admins, or superusers.
    """

    def has_permission(self, request, view):
        user = request.user

        # Allow superusers
        if user.is_superuser:
            return True

        # Allow financial admins and other admins
        if user.groups.filter(name__in=['fin_support', 'tech_support']).exists():
            return True

        # Otherwise, deny
        return False



class IsTicketOwnerOrSupport(BasePermission):
    """
    Allows access only to the ticket owner or the assigned support/admin.
    """

    def has_permission(self, request, view):
        ticket_id = view.kwargs.get('ticket_id')
        user = request.user

        from .models import Ticket  # import here to avoid circular import
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return False

        # Owner of the ticket
        if ticket.user == user:
            return True

        # Support/admin assigned by category
        if user.is_superuser:
            return True
        if user.groups.filter(name='fin_support').exists() and ticket.category == 'financial':
            return True
        if user.groups.filter(name='tech_support').exists() and ticket.category == 'technical':
            return True

        return False
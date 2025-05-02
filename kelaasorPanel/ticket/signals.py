from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Ticket

@receiver(post_save, sender=Message)
def update_ticket_status_on_message(sender, instance, created, **kwargs):
    if not created:
        return

    ticket = instance.ticket
    if ticket.status == 'closed':
        return

    if instance.user.is_staff:
        ticket.status = 'answered'
    else:
        ticket.status = 'unanswered'
    
    ticket.save()

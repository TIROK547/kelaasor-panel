import requests
from django.core.cache import cache
from celery import shared_task
from user.models import User
from .models import Ticket
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta

@shared_task
def alert_support(user_id, ticket_id, category):
    """
    Celery task to alert support admins via email about a new ticket.
    
    Args:
        user_id (int): ID of the user who created the ticket.
        ticket_id (int): ID of the ticket.
        category (str): Ticket category ('technical' or 'financial').
    """
    user = User.objects.get(id=user_id)
    ticket = Ticket.objects.get(id=ticket_id)
    send_email(user, category, ticket)

def send_email(user, category, ticket):
    """
    Helper function to send notification email to the appropriate support group.
    
    Args:
        user (User): The user who created the ticket.
        category (str): The ticket category.
        ticket (Ticket): The ticket instance.
    """
    group_name = ""
    if category == "technical":
        group_name = "tech_support"
    elif category == "financial":
        group_name = "fin_support"
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        print(f"Group '{category}' not found.")
        return
    
    admins = group.user_set.all()
    recipient_emails = [admin.email for admin in admins if admin.email]
    
    send_mail(
        subject=f'New {category} ticket from {user.phone_number}',
        message=f'Sender: {user.phone_number} (ID: {user.id})\nCategory: {category}\nTime: {ticket.date_created}',
        from_email='kelaasor.suport@gmail.com',
        recipient_list=recipient_emails,
        fail_silently=False,
    )
    print(recipient_emails)

@shared_task
def close_old_tickets():
    """
    Celery task to close tickets older than 7 days that are still open.
    
    Returns:
        str: Summary message indicating how many tickets were closed.
    """
    seven_days_ago = timezone.now() - timedelta(days=7)
    tickets = Ticket.objects.filter(
        status__in=['pending', 'answered', 'unanswered'],
        date_created__lt=seven_days_ago
    )
    updated_count = tickets.update(status='closed')
    return f"{updated_count} tickets closed"

import requests
from django.core.cache import cache
from celery import shared_task
from user.models import User
from .models import Ticket
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.models import Group

@shared_task
def alert_support(user_id, ticket_id, category):
    user = User.objects.get(id=user_id)
    ticket = Ticket.objects.get(id=ticket_id)
    send_login_email(user, category, ticket)

def send_login_email(user, category, ticket):
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
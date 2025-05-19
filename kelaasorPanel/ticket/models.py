from django.db import models
from user.models import User

class Ticket(models.Model):
    """
    Model representing a support ticket submitted by a user.
    
    Attributes:
        user (User): The user who submitted the ticket.
        date_created (datetime): The timestamp when the ticket was created.
        category (str): The category of the ticket, e.g., 'financial' or 'technical'.
    """
    CATEGORY_CHOICES = [
        ('financial', 'مالی'),
        ('technical', 'فنی'),
    ]
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='financial'
    )

class Message(models.Model):
    """
    Model representing a message within a support ticket conversation.

    Attributes:
        user (User): The sender of the message.
        text (str): The content of the message.
        attachment (Image): Optional image file uploaded with the message.
        ticket (Ticket): The ticket this message belongs to.
        date_sended (datetime): The timestamp when the message was sent.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1500)
    attachment = models.ImageField(upload_to='tickets/', blank=True, null=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='messages')
    date_sended = models.DateTimeField(auto_now_add=True)

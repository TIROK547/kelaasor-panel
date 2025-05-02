from django.db import models
from user.models import User

class Ticket(models.Model):
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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1500)
    attachment = models.ImageField(upload_to='tickets/', blank=True, null=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='messages')
    date_sended = models.DateTimeField(auto_now_add=True)
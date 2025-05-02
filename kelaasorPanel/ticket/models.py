from django.db import models
from user.models import User

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('financial', 'مالی'),
        ('technical', 'فنی'),
    ]

    STATUS_CHOICES = [
        ('pending', 'درحال بررسی'),
        ('answered', 'پاسخ داده شده'),
        ('unanswered', 'پاسخ داده نشده'),
        ('closed', 'بسته شده'),
    ]
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='financial'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1500)
    attachment = models.ImageField(upload_to='tickets/', blank=True, null=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    date_sended = models.DateTimeField(auto_now_add=True)
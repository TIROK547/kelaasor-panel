from django.db import models
from user.models import User

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('financial', 'مالی'),
        ('technical', 'فنی'),
    ]
    
    
    title = models.CharField(max_length=255)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='financial'
    )
    attachment = models.ImageField(upload_to='tickets/', blank=True, null=True)
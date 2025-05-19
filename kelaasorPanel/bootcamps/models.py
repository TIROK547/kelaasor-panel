from django.db import models
from django.core.exceptions import ValidationError
from user.models import User


class BootCampCategory(models.Model):
    """
    Represents a category for bootcamps with a specific type (in-person or online).
    """
    name = models.CharField(max_length=100)
    IN_PERSON = 'in_person'
    ONLINE = 'online'
    TYPE_CHOICES = [
        (IN_PERSON, 'حضوری'),
        (ONLINE, 'آنلاین'),
    ]
    bootcamp_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def __str__(self):
        return self.name 


class BootCamp(models.Model):
    """
    Represents a bootcamp with its metadata such as category, type, dates, capacity, and participants.
    """
    IN_PERSON = 'in_person'
    ONLINE = 'online'
    TYPE_CHOICES = [
        (IN_PERSON, 'حضوری'),
        (ONLINE, 'آنلاین'),
    ]

    STATE_CHOICES = [
        ('pre_registration', 'پیش‌ثبت‌نام'),
        ('registration_open', 'در حال ثبت‌نام'),
        ('in_progress', 'در حال برگزاری'),
        ('completed', 'برگزار شده'),
        ('canceled', 'لغو شده'),
    ]

    title = models.CharField(max_length=100)
    category = models.ForeignKey(BootCampCategory, on_delete=models.PROTECT, related_name='bootcamps')
    bootcamp_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    bootcamp_state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pre_registration')
    start_date = models.DateField()
    end_date = models.DateField()
    day_time = models.TimeField()
    day_of_weeks = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
    participants = models.ManyToManyField(User, through='BootCampParticipant', related_name='bootcamp_roles')

    def __str__(self):
        return self.title

    def clean(self):
        """
        Ensures that the start date is not after the end date and 
        that the bootcamp type matches the category type.
        """
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError("تاریخ شروع نمی‌تواند بعد از تاریخ پایان باشد.")
        
        if self.category and self.bootcamp_type != self.category.bootcamp_type:
            raise ValidationError("نوع بوت‌کمپ باید با نوع دسته‌بندی آن مطابقت داشته باشد.")


class BootCampParticipant(models.Model):
    """
    Represents a participant in a bootcamp, with a specific role (student, teacher, or mentor).
    """
    ROLE_CHOICES = [
        ('student', 'دانشجو'),
        ('teacher', 'مدرس'),
        ('mentor', 'منتور'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(BootCamp, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'bootcamp', 'role')

    def __str__(self):
        return f"{self.user} as {self.role} in {self.bootcamp}"


class BootCampsJoinRequest(models.Model):
    """
    Represents a request by a user to join a bootcamp with a specific payment plan.
    """
    PLAN_FULL = 'full'
    PLAN_INSTALLMENT = 'installment'

    PLAN_CHOICES = [
        (PLAN_FULL, 'پرداخت کامل'),
        (PLAN_INSTALLMENT, 'پرداخت اقساطی'),
    ]
    
    STATE_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="pending")
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    bootCamp = models.ForeignKey(to=BootCamp, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    
    @property
    def get_final_price(self):
        """
        Calculates the final price for the bootcamp based on the selected payment plan.
        An installment plan adds a 10% surcharge.
        """
        final_price = self.bootCamp.price
        if self.plan == self.PLAN_INSTALLMENT:
            return int(final_price * 1.1)
        return final_price

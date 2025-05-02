from django.db import models
from django.core.exceptions import ValidationError
from user.models import User


class BootCampCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BootCamp(models.Model):
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
        if self.start_date > self.end_date:
            raise ValidationError("تاریخ شروع نمی‌تواند بعد از تاریخ پایان باشد.")


class BootCampParticipant(models.Model):
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

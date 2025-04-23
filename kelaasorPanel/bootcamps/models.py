from django.db import models


class BootCamp(models.Model):
    title = models.CharField(max_length=20)


class InPersonBootCamp(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(to=BootCamp, on_delete=models.PROTECT)
    start_date = models.DateField()
    day_time = models.TimeField()
    day_of_weeks = models.CharField(max_length=50)
    end_date = models.DateField()
    capacity = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
    
    
class OnlineBootCamp(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(to=BootCamp, on_delete=models.PROTECT)
    start_date = models.DateField()
    day_time = models.TimeField()
    day_of_weeks = models.CharField(max_length=50)
    end_date = models.DateField()
    capacity = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
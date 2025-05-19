from django.db import models
from bootcamps.models import BootCamp, BootCampsJoinRequest
from user.models import User


class Factor(models.Model):
    """
    Represents a financial record associated with a user's join request to a bootcamp.
    """
    bootcamp = models.ForeignKey(BootCamp, on_delete=models.CASCADE, related_name='factors')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factors')
    request = models.ForeignKey(BootCampsJoinRequest, on_delete=models.CASCADE, related_name='factors')
    paid = models.BooleanField(default=False)

    @property
    def amount(self):
        """
        Returns the final price the user needs to pay based on the selected payment plan.
        """
        return self.request.get_final_price


class Payment(models.Model):
    """
    Represents a payment made by a user towards a specific factor (invoice).
    """
    STATE_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="pending")
    image = models.ImageField(upload_to='payments/')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveBigIntegerField()

    def mark_as_paid(self):
        """
        Marks this payment as accepted and checks if the total accepted payments cover the factor amount.
        If fully paid, sets the factor as paid and adds the user as a student to the bootcamp if not already added.

        Returns:
            "paid" if the factor is fully paid,
            "not paid" otherwise.
        """
        self.state = 'accepted'
        self.save()
        total = sum(payment.amount for payment in self.factor.payments.filter(state='accepted'))
        if total >= self.factor.amount:
            self.factor.paid = True
            self.factor.save()
            
            participants = self.factor.bootcamp.participants
            if not participants.filter(user=self.factor.user).exists():
                participants.create(
                    user=self.factor.user,
                    role='student',
                    bootcamp=self.factor.bootcamp
                )
                
            return "paid"
        return "not paid"

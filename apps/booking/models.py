from django.db import models

from account.models import CustomUser
from main.models import Stadium


class Booking(models.Model):
    stadium = models.ForeignKey(Stadium, related_name='bookings', on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, related_name='bookings', blank=True, null=True,
                             on_delete=models.SET_NULL)
    booking_start_time = models.DateTimeField()
    booking_end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.stadium.name
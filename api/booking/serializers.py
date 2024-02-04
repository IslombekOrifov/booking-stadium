from rest_framework import serializers

from apps.booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['stadium', 'user', 'booking_start_time', 
                  'booking_end_time', 'created']

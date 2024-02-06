from rest_framework import serializers

from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['stadium', 'user', 'booking_start_time', 
                  'booking_end_time', 'created']
        extra_kwargs = {
            'created': {'read_only': True},
        }

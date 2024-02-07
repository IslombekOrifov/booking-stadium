from rest_framework import serializers

from booking.models import Booking
from api.main.serializers import BookedStadiumSerializer
from api.account.serializers import CustomUserBookingSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['stadium', 'user', 'booking_start_time', 
                  'booking_end_time', 'created']
        extra_kwargs = {
            'user': {'read_only': True},
            'created': {'read_only': True},
        }
        

class UserBookedSerializer(serializers.ModelSerializer):
    stadium = BookedStadiumSerializer()
    class Meta:
        model = Booking
        fields = ['stadium', 'booking_start_time',
                  'booking_end_time', 'created']
        extra_kwargs = {
            'created': {'read_only': True},
        }
        

class OwnerBookingSerializer(serializers.ModelSerializer):
    stadium = BookedStadiumSerializer()
    user = CustomUserBookingSerializer()
    class Meta:
        model = Booking
        fields = ['stadium', 'user', 'booking_start_time', 
                  'booking_end_time', 'created']
        extra_kwargs = {
            'created': {'read_only': True},
        }

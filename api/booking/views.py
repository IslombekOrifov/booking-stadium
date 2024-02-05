from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .serializers import BookingSerializer

from booking.models import Booking


class BookingListAPIView(APIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    

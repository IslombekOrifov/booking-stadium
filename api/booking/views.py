from rest_framework.generics import ListAPIView

from .serializers import BookingSerializer

from apps.booking.models import Booking


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

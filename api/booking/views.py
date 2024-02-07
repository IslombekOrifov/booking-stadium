from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    BookingCreateSerializer, UserBookedSerializer,
    OwnerBookingSerializer
)
from api.common.pagination import CustomPagination
from booking.models import Booking


class UserBookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = UserBookedSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Booking.objects.filter(user=self.request.user).select_related('stadium').order_by('-booking_end_time')
        return queryset
    
    
class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = OwnerBookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = {
        'stadium__id': ['exact'],
        'booking_start_time': ['gte', 'lte'], 
        'booking_end_time': ['gte', 'lte'], 
    }
    
    def get_queryset(self):
        queryset = Booking.objects.filter(stadium__user=self.request.user).select_related('stadium', 'user').order_by('-booking_start_time')
        return queryset
    

class BookingDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        booking = get_object_or_404(Booking, id=pk, stadium__user=request.user)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BookingCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=BookingCreateSerializer, responses={200: BookingCreateSerializer})
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            stadium = serializer.validated_data['stadium']
            start_time = serializer.validated_data['booking_start_time']
            end_time = serializer.validated_data['booking_end_time']
            bookings = Booking.objects.filter(
                stadium=stadium,
                booking_start_time__lt=end_time,
                booking_end_time__gt=start_time
            )
            if bookings.exists():
                return Response({'error': 'This stadium is booked for this time!'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
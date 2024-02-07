from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from rest_framework.generics import (
    ListAPIView, CreateAPIView,
)
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    StadiumSerializer, StadiumListSerializer, StadiumImageSerializer,
    StadiumCreateSerializer, RatingSerializer
)

from api.common.pagination import CustomPagination
from account.enums import UserRole
from main.models import Stadium, Rating
from booking.models import Booking


class StadiumCreateAPIView(CreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if request.user.role != UserRole.so.value:
            return Response({'status': "You can't create a stadium"}, status=status.HTTP_400_BAD_REQUEST)
        images = request.data.dict().pop('images', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, images)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, images):
        serializer.save(user=self.request.user)
        if not images:
            images_serializer = StadiumImageSerializer(data=images, many=True)
            images_serializer.is_valid(raise_exception=True)
            images_serializer.save(stadium=serializer.instance)
            

class StadiumUpdateAPIView(UpdateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Stadium, user=request.user, id=self.kwargs['pk'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
            
class StadiumImageAddAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        stadium = get_object_or_404(Stadium, user=request.user, id=pk)
        images_serializer = StadiumImageSerializer(data=request.FILES)
        images_serializer.is_valid(raise_exception=True)
        images_serializer.save(stadium=stadium)
        return Response(status=status.HTTP_201_CREATED)


class OwnerStadiumListAPIView(ListAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return Stadium.objects.filter(user=self.request.user)
    
    
class StadiumListAPIView(ListAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    pagination_class = CustomPagination

    def get_queryset(self):

        start_time_str = self.request.GET.get('start_time')
        end_time_str = self.request.GET.get('end_time')

        if start_time_str and end_time_str:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

            booked_stadiums = Booking.objects.filter(
                Q(booking_start_time__lt=start_time, booking_end_time__gt=start_time) |
                Q(booking_start_time__lt=end_time, booking_end_time__gt=end_time)
            ).values_list('stadium_id', flat=True)
        else:
            booked_stadiums = []

        queryset = Stadium.objects.all().exclude(id__in=booked_stadiums).annotate(
            rating=Avg('ratings__score')
        ).order_by('-rating')
        if self.request.GET.get('latitude', False) and self.request.GET.get('longitude', False):
            user_latitude = float(self.request.GET.get('latitude'))
            user_longitude = float(self.request.GET.get('longitude'))
            user_location = Point(user_longitude, user_latitude, srid=4326)
            queryset = queryset.annotate(
                distance=Distance('location', user_location)
            ).exclude(id__in=booked_stadiums).order_by('distance')
        return queryset
        
        
class StadiumDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: StadiumSerializer})
    def get(self, request, pk):
        try:
            stadium = Stadium.objects.filter(id=pk).prefetch_related('images').first().annotate(
                rating=Avg('ratings__score')
            )
        except Stadium.DoesNotExist:
            raise Http404
        serializer = StadiumSerializer(stadium)
        return Response(serializer.data)


class RatingCreateOrUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(request_body=RatingSerializer)
    def post(self, request, pk):
        stadium = get_object_or_404(Stadium, id=pk)
        try:
            rating = Rating.objects.get(stadium=stadium, user=request.user)
            serializer = RatingSerializer(instance=rating, data=request.data)
        except Rating.DoesNotExist:
            serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(stadium=stadium, user=request.user)
        
        return Response(status=status.HTTP_201_CREATED)
from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Avg, Q, F, Func
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models.functions import Cast

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView,
)
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    StadiumSerializer, StadiumListSerializer, StadiumImageSerializer,
    StadiumCreateSerializer, RatingSerializer
)

from main.models import Stadium
from booking.models import Booking


class CustomPagination(PageNumberPagination):
    page_size=2
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'showing_count': self.page_size,
            'results': data
        })


class StadiumCreateAPIView(CreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
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
    def get(self, request, pk):
        try:
            stadium = Stadium.objects.filter(id=pk).prefetch_related('images').first().annotate(
                rating=Avg('ratings__score')
            )
        except Stadium.DoesNotExist:
            raise Http404
        serializer = StadiumSerializer(stadium)
        return Response(serializer.data)


class RatingAddAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        stadium = get_object_or_404(Stadium, id=pk)
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(stadium=stadium, user=request.user)
        return Response(status=status.HTTP_201_CREATED)
        
from django.http import Http404
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView,
)
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    StadiumSerializer, StadiumListSerializer, StadiumImageSerializer,
    StadiumCreateSerializer
)

from main.models import Stadium


class StadiumCreateAPIView(CreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        images = request.data.pop('images', [])
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
    serializer_class = StadiumListSerializer
        
        
class StadiumDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            stadium = Stadium.objects.filter(id=pk).select_related('images').first()
        except Stadium.DoesNotExist:
            raise Http404
        serializer = StadiumSerializer(stadium)
        return Response(serializer.data)


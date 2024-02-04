from django.http import Http404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import StadiumSerializer, StadiumListSerializer

from apps.main.models import Stadium


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


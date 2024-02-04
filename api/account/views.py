from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CustomUserSerializer

from apps.account.models import CustomUser

        
class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


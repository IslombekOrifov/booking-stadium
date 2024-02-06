from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import (
    RegisterSerializer, CustomUserSerializer,
    UserChangePasswordSerializer
)

from account.models import CustomUser

        
class RegisterAPIView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'User succesfully created.'}, status=status.HTTP_201_CREATED)


class UserUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserDetailAPIView(APIView):
    
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class UserChangePasswordView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'Password successfully changed.'}, status=status.HTTP_200_OK)

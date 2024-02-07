from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    RegisterSerializer, CustomUserSerializer,
    UserChangePasswordSerializer
)

from account.models import CustomUser

        
class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'User succesfully created.'}, status=status.HTTP_201_CREATED)


class UserUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(request_body=CustomUserSerializer, responses={200: CustomUserSerializer})
    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(responses={200: CustomUserSerializer})
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class UserChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserChangePasswordSerializer
    
    @swagger_auto_schema(request_body=UserChangePasswordSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'Password successfully changed.'}, status=status.HTTP_200_OK)


class LogoutView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('refresh')
        if token:
            try:
                token_obj = OutstandingToken.objects.get(token=token)
                BlacklistedToken.objects.create(token=token_obj)
                return Response(status=status.HTTP_200_OK)
            except OutstandingToken.DoesNotExist:
                return Response({'error': 'Token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers

from apps.account.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 
                  'phone', 'photo']
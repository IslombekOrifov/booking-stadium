from rest_framework import serializers

from main.models import Stadium, StadiumImage


class StadiumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumImage
        fields = ['image']
        

class StadiumSerializer(serializers.ModelSerializer):
    images = StadiumImageSerializer(many=True)
    class Meta:
        model = Stadium
        fields = ['name', 'logo', 'address', 'description', 
                  'contact1', 'contact2', 'price', 
                  'start_working_time', 'end_working_time', 
                  'lat', 'long', 'images']
        

class StadiumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['name', 'logo', 'address', 'start_working_time', 
                  'end_working_time', 'lat', 'long']
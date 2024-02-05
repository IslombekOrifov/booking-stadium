from rest_framework import serializers

from main.models import Stadium, StadiumImage, Rating


class StadiumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumImage
        fields = ['image']
        

class StadiumSerializer(serializers.ModelSerializer):
    images = StadiumImageSerializer(many=True)
    rating = serializers.IntegerField()
    
    class Meta:
        model = Stadium
        fields = ['name', 'logo', 'address', 'description', 
                  'contact1', 'contact2', 'price', 
                  'start_working_time', 'end_working_time', 
                  'lat', 'long', 'images', 'rating']
        

class StadiumListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    class Meta:
        model = Stadium
        fields = ['id', 'name', 'logo', 'address', 'start_working_time', 
                  'end_working_time', 'lat', 'long', 'rating']
        

class StadiumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['name', 'logo', 'address', 'description', 
                  'contact1', 'contact2', 'price', 
                  'start_working_time', 'end_working_time', 
                  'lat', 'long']
        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']
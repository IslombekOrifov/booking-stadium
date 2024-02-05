from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

from .validators import phone_number_validator
from .services import upload_logo_path, upload_stadium_image

from account.models import CustomUser


class Stadium(gis_models.Model):
    user = models.ForeignKey(CustomUser, related_name='stadiums', on_delete=models.PROTECT)
    name = models.CharField(max_length=50, db_index=True)
    logo = models.ImageField(upload_to=upload_logo_path, blank=True, null=True)
    address = models.CharField(max_length=250, db_index=True)
    description = models.TextField(blank=True, null=True)
    contact1 = models.CharField(max_length=13, blank=True, null=True, db_index=True, validators=[phone_number_validator])
    contact2 = models.CharField(max_length=13, blank=True, null=True, db_index=True, validators=[phone_number_validator])
    price = models.PositiveIntegerField()
    start_working_time = models.TimeField()
    end_working_time = models.TimeField()
    lat = models.FloatField()
    long = models.FloatField()
    location = gis_models.PointField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if self.lat is not None and self.long is not None:
            self.location = Point(self.long, self.lat)
        super().save(*args, **kwargs)
    

class StadiumImage(models.Model):
    image = models.ImageField(upload_to=upload_stadium_image)
    stadium = models.ForeignKey(Stadium, related_name='images', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.stadium.name


class Rating(models.Model):
    score = models.PositiveIntegerField()
    stadium = models.ForeignKey(Stadium, related_name='ratings', 
                             on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='rated_stadiums', 
                             on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.score)
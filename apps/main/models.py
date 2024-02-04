from django.db import models

from .validators import phone_number_validator
from .services import upload_logo_path, upload_stadium_image

from account.models import CustomUser


class Stadium(models.Model):
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
    lat = models.DecimalField(max_digits=22, decimal_places=18, default=0)
    long = models.DecimalField(max_digits=22, decimal_places=18, default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    

class StadiumImage(models.Model):
    image = models.ImageField(upload_to=upload_stadium_image)
    stadium = models.ForeignKey(Stadium, related_name='images', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.stadium.name


class Rating(models.Model):
    score = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, related_name='rated_stadiums', 
                             on_delete=models.SET_NULL, blank=True, mull=True)
    
    def __str__(self) -> str:
        return str(self.score)
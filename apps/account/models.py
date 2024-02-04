from django.db import models
from django.contrib.auth.models import AbstractUser

from .services import upload_avatar_path

from main.validators import phone_number_validator

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to=upload_avatar_path, blank=True, null=True)
    phone_number = models.CharField(max_length=13,
                                    blank=True,
                                    null=True,
                                    unique=True,
                                    db_index=True,
                                    validators=[phone_number_validator])
    REQUIRED_FIELDS = []
        
    def __str__(self) -> str:
        return self.username
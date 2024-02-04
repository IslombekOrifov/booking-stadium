from django.contrib import admin

from .models import Stadium, StadiumImage, Rating


admin.site.register(Stadium)
admin.site.register(StadiumImage)
admin.site.register(Rating)
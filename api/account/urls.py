from django.urls import path

from .views import (
    UserDetailAPIView, 
)


urlpatterns = [
    path('detail/', UserDetailAPIView.as_view()),
]

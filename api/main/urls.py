from django.urls import path

from .views import (
    StadiumListAPIView, StadiumDetailAPIView
)


urlpatterns = [
    path('list/', StadiumListAPIView.as_view()),
    path('detail/<int:pk>/', StadiumDetailAPIView.as_view()),
]

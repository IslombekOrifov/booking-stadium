from django.urls import path

from .views import (
    StadiumCreateAPIView,
    StadiumListAPIView, StadiumDetailAPIView,
    RatingCreateOrUpdateAPIView
)


urlpatterns = [
    path('create/', StadiumCreateAPIView.as_view()),
    path('list/', StadiumListAPIView.as_view()),
    path('detail/<int:pk>/', StadiumDetailAPIView.as_view()),
    path('rate/<int:pk>/', RatingCreateOrUpdateAPIView.as_view()),
]

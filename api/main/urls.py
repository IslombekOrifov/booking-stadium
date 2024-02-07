from django.urls import path

from .views import (
    StadiumCreateAPIView, StadiumImageAddAPIView,
    StadiumUpdateAPIView, StadiumListAPIView, 
    StadiumDetailAPIView, RatingCreateOrUpdateAPIView, 
    OwnerStadiumListAPIView,
)


urlpatterns = [
    path('create/', StadiumCreateAPIView.as_view()),
    path('update/<int:pk>/', StadiumUpdateAPIView.as_view()),
    path('image/add/<int:pk>/', StadiumImageAddAPIView.as_view()),
    path('owner/list/', OwnerStadiumListAPIView.as_view()),
    path('list/', StadiumListAPIView.as_view()),
    path('detail/<int:pk>/', StadiumDetailAPIView.as_view()),
    path('rate/<int:pk>/', RatingCreateOrUpdateAPIView.as_view()),
]

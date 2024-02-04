from django.urls import path

from .views import (
    BookingListAPIView, 
)


urlpatterns = [
    path('list/', BookingListAPIView.as_view()),
]

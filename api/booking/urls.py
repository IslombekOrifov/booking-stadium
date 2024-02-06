from django.urls import path

from .views import (
    UserBookingListAPIView, BookingListAPIView,
    BookingDestroyAPIView, BookingCreateAPIView
)


urlpatterns = [
    path('user/list/', UserBookingListAPIView.as_view()),
    path('admin/list/', BookingListAPIView.as_view()),
    path('delete/', BookingDestroyAPIView.as_view()),
    path('create/', BookingCreateAPIView.as_view()),
]

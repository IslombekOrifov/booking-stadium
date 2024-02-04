from django.urls import path, include


urlpatterns = [
    path('main/', include('api.main.urls')),
    path('booking/', include('api.booking.urls')),
]

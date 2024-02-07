from django.urls import path, include


urlpatterns = [
    path('account/', include('api.account.urls')),
    path('main/', include('api.main.urls')),
    path('booking/', include('api.booking.urls')),
]

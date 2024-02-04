from django.urls import path, include


urlpatterns = [
    path('main/', include('main.urls', namespace='main')),
]

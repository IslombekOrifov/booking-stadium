from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserDetailAPIView, RegisterAPIView,
    UserUpdateAPIView
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('detail/<int:pk>/', UserDetailAPIView.as_view()),
    path('reister/', RegisterAPIView.as_view()),
    path('update/', UserUpdateAPIView.as_view()),

]

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserDetailAPIView, RegisterAPIView,
    UserUpdateAPIView, LogoutView, 
    UserChangePasswordView
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('detail/<int:pk>/', UserDetailAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('update/', UserUpdateAPIView.as_view()),
    path('update/', UserChangePasswordView.as_view()),
    path('logout/', LogoutView.as_view()),

]

from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny
from .Serializers import CustomTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token-refresh'),
]
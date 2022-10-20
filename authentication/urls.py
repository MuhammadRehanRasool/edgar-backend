from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path("users", views.CustomUserCreate.as_view(), name="users"),
    path("token/obtain", views.MyTokenObtainPairView.as_view(), name="token_create"),
    path("token/refresh", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
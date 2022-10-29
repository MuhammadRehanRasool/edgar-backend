from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path("testing", views.testing, name="testing"),
    path("topics", views.topics, name="topics"),
    path("plans", views.plans, name="plans"),
]
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path("makePayment", views.makePayment, name="makePayment"),
    path("topics", views.topics, name="topics"),
    path("plans", views.plans, name="plans"),
    path("subscriptions", views.subscriptions, name="subscriptions"),
    path("mysubscriptions", views.mysubscriptions, name="mysubscriptions"),
]
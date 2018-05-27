from django.contrib import admin
from django.urls import path, include 
from .views import authenticate_user

urlpatterns = [
    path('auth', authenticate_user)
]

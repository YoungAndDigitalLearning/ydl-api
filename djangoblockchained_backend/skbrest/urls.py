from django.contrib import admin
from django.urls import path, include 
from .views import authenticate_user
from .api import CreateUserView

urlpatterns = [
    path('auth', authenticate_user),
    path('register', CreateUserView.as_view())
]

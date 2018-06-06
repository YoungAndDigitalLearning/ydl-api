from django.contrib import admin
from django.urls import path, include 
from rest_framework_jwt.views import obtain_jwt_token

from .views import CourseAPIView, CreateUserAPIView

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('courses/', CourseAPIView.as_view()),
    path('users/', CreateUserAPIView.as_view())
]

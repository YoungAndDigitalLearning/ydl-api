from django.contrib import admin
from django.urls import path, include 
from rest_framework_jwt.views import obtain_jwt_token

from .views import CourseAPIView, ListCreateUserAPIView, activate, LonngLongListApiView, DetailUserAPIView, DetailCourseAPIView

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('courses/', CourseAPIView.as_view()),
    path('courses/<int:pk>', DetailCourseAPIView.as_view()),
    path('students/', LonngLongListApiView.as_view()),
    path('users/', ListCreateUserAPIView.as_view()),
    path('users/<int:pk>', DetailUserAPIView.as_view()),
    path('activate/<uidb64>/<token>/', activate)
]
 
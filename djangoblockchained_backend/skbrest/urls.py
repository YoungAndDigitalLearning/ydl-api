from django.contrib import admin
from django.urls import path, include 
from rest_framework_jwt.views import obtain_jwt_token

from .views import CourseAPIView, ListCreateUserAPIView, activate, LonngLongListApiView, DetailUserAPIView, DetailCourseAPIView, ListCreateResourceAPIView, ListCreateAnouncementAPIView, LimitListAnouncementAPIView

user_list = ListCreateUserAPIView.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = ListCreateUserAPIView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('courses/', CourseAPIView.as_view()),
    path('courses/<int:pk>', DetailCourseAPIView.as_view()),
    path('students/', LonngLongListApiView.as_view()),
    path('users/', user_list),
    path('users/<int:pk>', user_detail),
    path('activate/<uidb64>/<token>/', activate),
    path('resources/', ListCreateResourceAPIView.as_view()),
    path('anouncements/', ListCreateAnouncementAPIView.as_view()), # use ...anouncements/?limit=<int:limit>... for limited An 
]
 
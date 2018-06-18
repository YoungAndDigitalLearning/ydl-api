from django.contrib import admin
from django.urls import path, include 
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view

from .views import CourseAPIView, ListCreateUserViewSet, activate, StudentListApiView, DetailUserAPIView, DetailCourseAPIView, \
ListCreateResourceAPIView, ListCreateAnouncementAPIView, LimitListAnouncementAPIView, render_email
# import .views 

from django.conf import settings

user_list = ListCreateUserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = ListCreateUserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

schema_view = get_swagger_view(title='Y&D Learning API')

urlpatterns = [
    path('', schema_view),
    path('token/auth/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('courses/', CourseAPIView.as_view(), name="course-list"),
    path('courses/<int:pk>', DetailCourseAPIView.as_view()),
    path('students/', StudentListApiView.as_view()),
    path('users/', user_list, name="user-list"),
    path('users/<int:pk>', user_detail),
    path('activate/<uidb64>/<token>/', activate),
    path('resources/', ListCreateResourceAPIView.as_view()),
    path('anouncements/', ListCreateAnouncementAPIView.as_view()), # use ...anouncements/?limit=<int:limit>... for limited An 
]


if settings.DEBUG:
    urlpatterns += [
        path('html', render_email),
    ]
 
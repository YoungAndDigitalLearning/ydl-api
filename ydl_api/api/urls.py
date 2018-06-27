from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import include, url

from .views import UserViewSet, activate, StudentListApiView, DetailUserAPIView, DetailCourseAPIView, \
    ListCreateResourceAPIView, ListCreateAnnouncementAPIView, render_email, PostViewSet, \
    MessageViewSet, CourseViewSet
# import .views

from django.conf import settings

# API (Swagger)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Seperate from url pattern
# User
user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Post
post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Message
message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Course
course_list = CourseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
course_detail = CourseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

"""Swagger API shema view
"""
schema_view = get_schema_view(
    openapi.Info(
        title="Y&D Learning API",
        default_version='v1',
        description="Rest API Documentation for Y&D Learning",
        terms_of_service="https://ydlearning.com/sites/impressum.html",
        contact=openapi.Contact(email="admin@ydlearning.com"),
        license=openapi.License(name=""),  # License
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

"""Urlpatterns to define reachable urls
"""
urlpatterns = [
    #path('', schema_view),
    path('token/auth/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('students/', StudentListApiView.as_view()),
    path('users/', user_list, name="user-list"),
    path('users/<int:pk>', user_detail),
    path('activate/<uidb64>/<token>/', activate),
    path('resources/', ListCreateResourceAPIView.as_view()),
    # use ...announcements/?limit=<int:limit>... for limited An
    path('announcements/', ListCreateAnnouncementAPIView.as_view()),
    path('payments/', include('payments.urls')),
    path('posts/', post_list, name="post-list"),
    path('posts/<int:pk>', post_detail, name="post-detail"),
    path('courses/', course_list, name="course-list"),
    path('courses/<int:pk>', course_detail, name="course-detail"),
    path('messages/', message_list, name="message-list"),
    path('messages/<int:pk>', message_detail),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=None), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=None),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=None), name='schema-redoc'),
]

"""Url to try out new html designs
"""
if settings.DEBUG:
    urlpatterns += [
        path('html', render_email),
    ]

from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import include, url

from .views import CourseAPIView, UserViewSet, activate, StudentListApiView, DetailUserAPIView, DetailCourseAPIView, \
ListCreateResourceAPIView, ListCreateAnnouncementAPIView, LimitListAnnouncementAPIView, render_email, PostViewSet, CourseAllAPIView
# import .views 


from django.conf.urls import (
  handler400, handler403, handler404, handler500)

from api.views import error404
handler404 = error404


from django.conf import settings

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

#schema_view = get_swagger_view(title='Y&D Learning API')

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    #path('', schema_view),
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
    path('announcements/', ListCreateAnnouncementAPIView.as_view()), # use ...announcements/?limit=<int:limit>... for limited An 
    path('payments/', include('payments.urls')),
    path('posts/', post_list, name="post-list"),
    path('posts/<int:pk>', post_detail, name="post-detail"),
    path('courses/free/', CourseAllAPIView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += [
        path('html', render_email),
    ]
 
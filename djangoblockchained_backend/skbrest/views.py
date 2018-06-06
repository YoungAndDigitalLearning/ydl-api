from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth.models import User  # If used custom user model
# Our imports
from .models import Course
from .serializers import UserSerializer, CourseSerializer


class CreateUserAPIView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class CourseAPIView(ListAPIView):
    model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user.id)

    # Debug
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]

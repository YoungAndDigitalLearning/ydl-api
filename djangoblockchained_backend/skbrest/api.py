from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User # If used custom user model

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer
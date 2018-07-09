from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from quiz import models as m
from quiz import serializers

# Create your views here.
class TestViewSet(ModelViewSet):
    serializer_class = serializers.TestSerializer
    queryset = m.Test.objects.all()

    permission_classes = [
        permissions.AllowAny
    ]
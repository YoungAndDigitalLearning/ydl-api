from rest_framework import serializers
from django.contrib.auth.models import User  # If used custom user model
from .models import Student, Teacher, Course
from django.core.mail import send_mail


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        student = Student.objects.create(user=user)
        student.save()

        send_mail(
            'Verify email adress for Y&D Learning',
            'Dear ' + user.username + ', \nThank you for using Y&D Learning. \nPlease confirm your Email Adress. \nLink: https://ydlearning.ml',
            'ydlearning.service@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return user

    class Meta:
        model = User
        fields = ["password", "username", "email"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

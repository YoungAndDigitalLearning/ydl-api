from rest_framework import serializers
from django.contrib.auth.models import User  # If used custom user model
from .models import Student, Teacher, Course
from django.core.mail import send_mail

# Email Stuff A
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework_jwt.settings import api_settings
from django.conf import settings
# Email Stuff E


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

        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        send_mail(
            # Subject
            'Verify email adress for Y&D Learning',
            # Content
            'Dear ' + user.username + ', \n'+
            'Thank you for using Y&D Learning. \n' +
            'Please confirm your Email Adress. \n'+
            'Link: http://localhost:8000/api/activate/{}/{}'.format(uid, token) + '\n' +
            'Link expires in ' + str(settings.JWT_AUTH['JWT_EXPIRATION_DELTA']) + 'Minutes.',
            # Email send from
            'ydlearning.service@gmail.com',
            # Email send to
            [user.email],
            # fail silently
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

# -- coding: utf-8 --

from rest_framework import serializers
from .models import Student, Teacher, Course, Resource, Announcement, User
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
from django.core.mail import EmailMessage
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.template import Context
from django.template.loader import get_template
# Email Stuff E

from django.utils import timezone
 
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return jwt_encode_handler(jwt_payload_handler(obj))

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_student=True,
        )
        user.set_password(validated_data['password'])
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        html_template = get_template('api/verification_email.html')

        context = {
            'user':user.username,
            'link':'https://api.ydlearning.com/activate/{}/{}'.format(uid, token),
            'expires_in':str(settings.JWT_AUTH['JWT_EXPIRATION_DELTA']),
            'expires_time': ' hours',  # change plural!
            'logo_img_link':"https://lh3.googleusercontent.com/PL8M-2OhoDITza8WOCdveAax9yQuXzaDakaJHcivO1ZjJg5D1u0eb9gzgx8VSLlfVT4vitIV2GIPkc8OfGJrR6rpko1U8JuV4CAZ2p-gvc4NhVUthlbaEz9HcKwY98UFiwN79pzu=s742-no",
            'email_sendto':user.email,
            'ydl_email':"admin@ydlearning.com",
            'ydl_url':"https://www.ydlearning.com",
            'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
            'ydl_url_impr': "https://www.ydlearning.com/impressum.html",
            'ydl_url_prpol': "https://www.ydlearning.com/privacypolicy",
        }
        html = html_template.render(context)

        send_mail(
            # Subject
            '[Y&D Learning] Please verify your email address.',
            '',
            # Content
                # 
            # Email send from
            #'admin@ydlearning.com',
            'no-reply@ydlearning.com',
            # Email send to
            [user.email],
            # fail silently
            fail_silently=False,
            html_message = html,
        )

        return user

    class Meta:
        model = User
        fields = ["password", "username", "email", "token"]
        extra_kwargs = {
            'username': {'write_only': True, 'read_only': False},
            'email': {'write_only': True, 'read_only': False},
            'password': {'write_only': True, 'read_only': False},
        }

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__" 

# Nur für Get auf den User 
class LongUserSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):

        if obj.is_teacher:
            return TeacherSerializer(obj.teacher).data["course_set"]
        elif obj.is_student: 
            return StudentSerializer(obj.student ).data["course_set"]

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "last_login", "date_joined", "isEmailActivated", "courses", "is_teacher"]

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["user", "course_set"]

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["user", "course_set"]

class ResourceSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    # only return content if effective date is now or already passed 
    def get_content(self, obj):
        if obj.effective_from >= timezone.now():
            return self.context["request"].build_absolute_uri(obj.content.url)
        else:
            return None

    def get_size(self, obj):
        return obj.content.size

    class Meta:
        model = Resource
        fields = ["name", "uploaded", "effective_from", "uploader", "expires", "size", "content"]

class AnnouncementSerializer(serializers.ModelSerializer):
    author = LongUserSerializer(many = False, read_only = True)

    class Meta:
        model = Announcement
        fields = "__all__"    
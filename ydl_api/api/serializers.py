# -- coding: utf-8 --

from rest_framework import serializers
from .models import Student, Teacher, Course, Resource, Announcement, User, Post, Message, CalendarEntry, Week
from django.core.mail import send_mail
from django.db.models import Q

# Email Stuff A
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
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

class ResourceSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    uploader_name = serializers.CharField(source="uploader", read_only=True)
    
    def get_size(self, obj):
        return obj.content.size

    class Meta:
        model = Resource
        fields = "__all__"
        extra_kwargs = {
            "uploader": {"read_only": True}
        }

class UserSerializer(serializers.ModelSerializer):
    # sending back token for initial login
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

        # generate uid for activation email
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

        # generate jwt token manually (see drf jwt docs)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # load email template
        html_template = get_template('api/verification_email.html')

        context = {
            'user': user.username,
            'link': 'https://api.ydlearning.com/activate/{}/{}'.format(uid, token),
            'expires_in': str(settings.JWT_AUTH['JWT_EXPIRATION_DELTA']),
            'expires_time': ' hours',  # change plural!
            # 'logo_img_link':"",
            'email_sendto': user.email,
            'ydl_context': "Context Text",
            'ydl_email': "admin@ydlearning.com",
            'ydl_url': "https://www.ydlearning.com",
            'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
            'ydl_url_impr': "https://www.ydlearning.com/sites/impressum.html",
        }
        html = html_template.render(context)

        send_mail(
            # Subject
            '[Y&D Learning] Please verify your email address.',
            '',
            # Content
            #
            # Email send from
            # 'admin@ydlearning.com',
            'no-reply@ydlearning.com',
            # Email send to
            [user.email],
            # fail silently
            fail_silently=False,
            html_message=html,
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

class CalendarEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEntry
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    weeks = serializers.SerializerMethodField()
    resources = serializers.SerializerMethodField()
    tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="test_set")

    def get_resources(self, course):
        return [ResourceSerializer(resource).data for resource in Resource.objects.filter(course = course)]

    def get_posts(self, course):
        return [PostSerializer(post).data["id"] for post in Post.objects.filter(course=course, childs__isnull=True)]

    def get_events(self, course):
        return [CalendarEntrySerializer(entry).data for entry in course.calendarentry_set.all()]

    def get_weeks(self, course):
        return [WeekSerialzier(week).data for week in Week.objects.filter(course=course.id)]

    class Meta:
        model = Course
        fields = "__all__"

        extra_kwargs = {
            'teacher': {'write_only': False, 'read_only': True},
        }


# Nur für Get auf den User
class LongUserSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    def update(self, instance, validated_data, *args, **kwargs):
        if instance.email != validated_data.get('email', instance.email):
            instance.isEmailActivated = False

            uid = urlsafe_base64_encode(force_bytes(instance.pk)).decode()

            payload = jwt_payload_handler(instance)
            token = jwt_encode_handler(payload)

            html_template = get_template('api/verification_email.html')

            context = {
                'user': validated_data.get('username', instance.username),
                'link': 'https://api.ydlearning.com/activate/{}/{}'.format(uid, token),
                'expires_in': str(settings.JWT_AUTH['JWT_EXPIRATION_DELTA']),
                'expires_time': ' hours',  # change plural!
                # 'logo_img_link':"",
                'email_sendto': validated_data.get('email', instance.email),
                'ydl_context': "Context Text",
                'ydl_email': "admin@ydlearning.com",
                'ydl_url': "https://www.ydlearning.com",
                'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
                'ydl_url_impr': "https://www.ydlearning.com/sites/impressum.html",
            }
            html = html_template.render(context)
            send_mail(
                # Subject
                '[Y&D Learning] Please verify your email address.',
                '',
                # Content
                #
                # Email send from
                # 'admin@ydlearning.com',
                'no-reply@ydlearning.com',
                # Email send to
                [validated_data.get('email', instance.email)],
                # fail silently
                fail_silently=False,
                html_message=html,
            )

        super().update(instance, validated_data)

        return instance
        

    def get_courses(self, user):
        if user.is_teacher:
            return TeacherSerializer(user.teacher).data["courses"]
        elif user.is_student:
            return StudentSerializer(user.student).data["courses"]
        
    def get_messages(self, obj):
        messages = {}

        for message in Message.objects.filter(Q(receiver = obj) | Q(sender = obj)):
            if message.sender != obj:
                try:
                    messages[int(message.sender.id)].append(MessageSerializer(message).data)
                except KeyError:
                    messages[int(message.sender.id)] = [MessageSerializer(message).data]
            else:
                try:
                    messages[int(message.receiver.id)].append(MessageSerializer(message).data)
                except KeyError:
                    messages[int(message.receiver.id)] = [MessageSerializer(message).data]
        return messages


    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "last_login", "date_joined",
                  "isEmailActivated", "courses", "is_teacher", "messages"]  # "email", Debug (Dont show emails on website)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["user", "courses"]

        # make the user not changeable
        extra_kwargs = {
           "user": {"read_only": True}
        }


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    # courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="course_set")
    
    def get_courses(self, teacher):
        return [CourseSerializer(course).data["id"] for course in teacher.user.get_courses()]
           

    class Meta:
        model = Teacher
        fields = ["user", "courses"]

class AnnouncementSerializer(serializers.ModelSerializer):
    author = LongUserSerializer(many=False, read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    childs = serializers.SerializerMethodField()

    def get_childs(self, obj):
        for child in obj.childs.all():
            if obj.childs is not "":
                yield PostSerializer(child).data
            else:
                return None

    class Meta:
        model = Post
        fields = ["id", "title", "text", "date", "author", "course", "childs"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class WeekSerialzier(serializers.ModelSerializer):
     class Meta:
        model = Week
        fields = "__all__"

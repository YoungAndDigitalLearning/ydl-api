from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from django.contrib.auth.models import User  # If used custom user model
# Our imports
from .models import Course, Student, Resource, Anouncement, Teacher
from .serializers import UserSerializer, CourseSerializer, LongUserSerializer, StudentSerializer, ResourceSerializer, AnouncementSerializer

# Email Stuff A
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from django.core.exceptions import ObjectDoesNotExist
# Email Stuff E

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def render_email(request):
    context = {
        'user': 'Croozer',
        'link': '#',
        # change plural!
        'expires_in': '1:00:00',
        'expires_time': ' hours',
        'logo_img_link': "https://lh3.googleusercontent.com/PL8M-2OhoDITza8WOCdveAax9yQuXzaDakaJHcivO1ZjJg5D1u0eb9gzgx8VSLlfVT4vitIV2GIPkc8OfGJrR6rpko1U8JuV4CAZ2p-gvc4NhVUthlbaEz9HcKwY98UFiwN79pzu=s742-no",
        'email_sendto': 'Croozer@ydlearning.com',
        'ydl_email': "admin@ydlearning.com",
        'ydl_url': "www.ydlearning.com",
        'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
        'ydl_url_impr': "www.ydlearning.com/impressum",
        'ydl_url_prpol': "www.ydlearning.com/privacypolicy",
    }

    return render(request, "skbrest/verification_email.html", context)


def activate(request, uidb64, token):
    """
    Activates an account

    Arguments:
        request {[type]} -- [description]
        uidb64 {[type]} -- [description]
        token {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
        print("user: ", user)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    verifier = VerifyJSONWebTokenSerializer()
    # print("verifier:", verifier.validate({'token':token}))
    validated = None
    # verifier.validate({'token':token})
    try:
        validated = jwt_decode_handler(token)
    except:
        pass

    if user is not None and validated:
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class ListCreateUserAPIView(ModelViewSet):

    """ User Resource
    ---
    create_request_serializer: UserSerializer
    create_response_serializer: UserSerializer
    """

    model = User
    permission_classes = [
        permissions.AllowAny  # Or users can't register
    ]
    # serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
        # User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserSerializer
        else:
            return LongUserSerializer


class DetailUserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = LongUserSerializer


class DetailCourseAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseAPIView(ListAPIView):
    model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        student = None
        teacher = None

        # try to get student OR teacher
        try:
            student = Student.objects.get(user=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        try:
            teacher = Teacher.objects.get(user=self.request.user.id)
        except ObjectDoesNotExist:
            pass

        if teacher:
            return Course.objects.filter(teacher=teacher.id)
        elif student:
            return Course.objects.filter(students=student.id)

        #print("couse", Course.objects.all()[0].students.all())
        #print("couse", Course.objects.filter(students__id=19))
        # return Course.objects.filter(students=self.request.user.id)

    # Debug
    permission_classes = [
        permissions.AllowAny  # Or users can't register
    ]


class LonngLongListApiView(ListAPIView):
    model = Student
    serializer_class = StudentSerializer

    queryset = Student.objects.all()

    permission_classes = [
        permissions.AllowAny  # Or users can't register
    ]


class ListCreateResourceAPIView(ListCreateAPIView):
    model = Resource
    serializer_class = ResourceSerializer

    queryset = Resource.objects.all()


class ListCreateAnouncementAPIView(ListCreateAPIView):
    model = Anouncement
    serializer_class = AnouncementSerializer

    # queryset = Anouncement.objects.all()

    def get_queryset(self):
        if self.request.method == "GET":
            limit = self.request.GET.get("limit", None)
            if limit:
                return Anouncement.objects.all()[:int(limit)]
            else:
                return Anouncement.objects.all()

    # Everyone should see
    permission_classes = [
        permissions.AllowAny  # Or users can't register
    ]


class LimitListAnouncementAPIView(ListAPIView):
    model = Anouncement
    serializer_class = AnouncementSerializer

    def get_queryset(self):
        print("Quarks", self.kwargs["limit"])
        return Anouncement.objects.all()[:self.kwargs["limit"]]

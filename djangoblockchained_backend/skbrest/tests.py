
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, CoreAPIClient
from .models import User, Student, Teacher, Course
from rest_framework_jwt.settings import api_settings
import datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def createToken(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)

class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse("user-list")
        data = {
            'username': 'Hansi',
            'password': 'HansiPW',
            'email': 'hansi@mail.mail' 
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Hansi')
        self.assertEqual(User.objects.get().email, 'hansi@mail.mail')

class CourseTests(APITestCase):
    def setUp(self):
        self.teacher = Teacher(
            user = User.objects.create_user(
                username = "Croozer",
                email = "Croozer@Croozer.com"
            )
        )
        self.teacher.save()

        self.courses = Course(
            name = "Croozers Logic Course",
            teacher_id = self.teacher.user.id,
            description = "Keep Kroozin!",
            deadline = datetime.datetime.now(),
            student_count = 5,
            price = 0
        )
        self.courses.save()

        self.student = Student(
            user = User.objects.create_user(
                username = "Karsten",
                email = "Karsten@Karsten.com"
            )
        )
        self.student.courses.add(self.courses)
        self.student.save()
        

        # self.client = CoreAPIClient()
        self.token = createToken(self.student.user)
        print("Session",self.client.session.kwargs)
        #self.client.session.headers.update({'Authorization': self.token})

    def test_get_student_courses(self):
        url = reverse("course-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data, {"id": 5})
        
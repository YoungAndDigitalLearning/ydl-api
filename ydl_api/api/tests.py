
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
        # create one dummy teacher
        self.teacher = Teacher.objects.create(
            user = User.objects.create_user(
                username = "Croozer",
                email = "Croozer@Croozer.com"
            )
        )
        
        # create one dummy student
        self.student = Student.objects.create(
            user = User.objects.create_user(
                username = "Karsten",
                email = "Karsten@Karsten.com"
            )
        )

        # create courses
        self.courses = [
            Course.objects.create(
                name = "Croozers Logic Course",
                teacher_id = self.teacher.user.id,
                description = "Keep Kroozin!",
                deadline = datetime.datetime.now(),
                student_count = 5,
                price = 0
            ),
            Course.objects.create(
                name = "Mathematik",
                teacher_id = self.teacher.user.id,
                description = "Mein Mathe",
                deadline = datetime.datetime.now(),
                student_count = 5,
                price = 20
            )
        ]

        # assign student to course
        self.student.courses.add(self.courses[0])
        
        # create tokens for each user
        self.student_token = createToken(self.student.user)
        self.teacher_token = createToken(self.teacher.user)

        self.student_client = CoreAPIClient()
        self.student_client.session.headers.update({"Authentication": "JWT " + self.student_token})

    def test_get_student_courses(self):
        url = reverse("course-list")
        response = self.student_client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, url)
        print(response.data)
        self.assertEqual(response.data, {"id": 5})
        
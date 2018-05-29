from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.username

#class Admin()

#class Moderator()

class Course(models.Model):
    name = models.TextField()
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    student_count = models.IntegerField(validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



    
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('student')
        verbose_name = ('students')


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('teacher')
        verbose_name = ('teachers')


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('moderator')
        verbose_name = ('moderators')


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    student_count = models.IntegerField(validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('course')
        verbose_name = ('courses')


class Anouncement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Moderator, on_delete=models.CASCADE)
    date = models.DateField()
    image = models.ImageField()
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Anouncement')
        verbose_name = ('Anouncements')

class Resource(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded = models.DateTimeField()
    effective_from = models.DateTimeField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    expires = models.DateTimeField()
    size = models.FloatField()
    content = models.FileField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('resource')
        verbose_name = ('resources')

class CalendarEntry(models.Model):
    MATTER_CHOICES = (
        (PRESENTATION, 'Presentation'),
        (HOMEWORK, 'Homework'),
        (EXAM, 'Exam'),
    )
    date = models.DateField()
    matter = models.CharField(choices=MATTER_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
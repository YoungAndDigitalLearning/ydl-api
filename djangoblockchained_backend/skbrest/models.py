from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course')
    isEmailActivated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('student')
        verbose_name_plural = ('students')


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isEmailActivated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('teacher')
        verbose_name_plural = ('teachers')


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('moderator')
        verbose_name_plural = ('moderators')


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    student_count = models.IntegerField(validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)
    resources = models.ManyToManyField("Resource") 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('course')
        verbose_name_plural = ('courses')


class Anouncement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    image = models.ImageField()
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Anouncement')
        verbose_name_plural = ('Anouncements')
        ordering = ["-date"]


class Resource(models.Model):
    name = models.CharField(max_length=100)
    uploaded = models.DateTimeField()
    effective_from = models.DateTimeField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    expires = models.DateTimeField()
    content = models.FileField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('resource')
        verbose_name_plural = ('resources')

class CalendarEntry(models.Model):
    MATTER_CHOICES = (
        ('PRESENTATION', 'Presentation'),
        ('HOMEWORK', 'Homework'),
        ('EXAM', 'Exam'),
    )
    date = models.DateField()
    matter = models.CharField(choices=MATTER_CHOICES, max_length=12)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('calendar entry')
        verbose_name_plural = ('calendar entries')
    
    def __str__(self):
        return self.matter

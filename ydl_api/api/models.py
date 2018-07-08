from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import m2m_changed

from payments import PurchasedItem
from payments.models import BasePayment

# Email Stuff
from django.core.mail import EmailMessage
from django.template.loader import get_template


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

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    def upload_to(self, filename):
        return "images/profiles/{}/{}".format(self.id, filename)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    isEmailActivated = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True)
    languages = models.ForeignKey(
        Language, on_delete=models.CASCADE, blank=True, null=True)
    credit = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    def get_courses(self):
        if self.is_teacher and self.is_student:
            return Course.objects.filter(Q(teacher=self.id) | Q(student=self.id)).distinct() 
        elif self.is_teacher:
            return Course.objects.filter(teacher=self.id)
        elif self.is_student:
            return Course.objects.filter(student=self.id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_student:
            student = Student(user=self)
            student.save()
        else:
            if hasattr(self, 'student'):
                self.student.delete()
        if self.is_teacher:
            teacher = Teacher(user=self)
            teacher.save()
        else:
            if hasattr(self, 'teacher'):
                self.teacher.delete()

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    courses = models.ManyToManyField('Course', blank=True)
    # paid_courses = models.ManyToManyField('Course', blank = True)

    def __str__(self):
        return str(self.user)
    
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #    super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    #    if "course" in update_fields:
    #        print("sda", self.courses)



    class Meta:
        verbose_name = ('student')
        verbose_name_plural = ('students')


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = ('teacher')
        verbose_name_plural = ('teachers')


class Moderator(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = ('moderator')
        verbose_name_plural = ('moderators')

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    student_count = models.IntegerField(
        validators=[MinValueValidator(0)], default=0)
    created = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)
    resources = models.ManyToManyField("Resource", blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = ('course')
        verbose_name_plural = ('courses')

def resources_changed(sender, **kwargs):
    action = kwargs.get("action", "None")
    instance = kwargs.get("instance", None)
    if action == "post_add":
        if instance:
            course_students = instance.student_set.all()
            print("us", course_students)
            students_username = [student.user.username for student in course_students]
            students_emails = [student.user.email for student in course_students]
            print("usn", students_username)
            print("em", students_emails)

            html_template = get_template('api/ressource_save.html')
            context = {
                #'user': self.objects user.username,
                #'link': 'https://api.ydlearning.com/activate/{}/{}'.format(uid, token),
                #'expires_in': str(settings.JWT_AUTH['JWT_EXPIRATION_DELTA']),
                #'expires_time': ' hours',  # change plural!
                # 'logo_img_link':"",
                #'email_sendto': user.email,
                #'ydl_context': "Context Text",
                #'ydl_email': "admin@ydlearning.com",
                #'ydl_url': "https://www.ydlearning.com",
                #'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
                #'ydl_url_impr': "https://www.ydlearning.com/sites/impressum.html",
            }
            html = html_template.render(context)
            email = EmailMessage(
                # Subject:
                '[Y&D Learning] New resource.',
                # Body / Content ==> html_message:
                html,
                # Email send from:
                'no-reply@ydlearning.com',
                # Email send to:
                [students_emails.pop()],
                # bcc
                students_emails,
            ) 
            email.content_subtype = "html" 
            email.send(fail_silently=False)   

        # resource has been updated

m2m_changed.connect(resources_changed, sender=Course.resources.through)

# class PaidCourse(models.Model):

class Week(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    week = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=4096)

    def __str__(self):
        return self.content[:20]

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def upload_to(self, filename):
        return "images/announcements/{}/{}".format(self.id, filename)

    image = models.ImageField(upload_to=upload_to, blank=True)

    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Announcement')
        verbose_name_plural = ('announcements')
        ordering = ["-date"]


class Resource(models.Model):
    name = models.CharField(max_length=100)
    uploaded = models.DateTimeField(auto_now_add=True)
    effective_from = models.DateTimeField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    expires = models.DateTimeField()
#   content

    def upload_to(self, filename):
        return "resources/{}/{}".format(self.uploader.id, filename)

    content = models.FileField(upload_to=upload_to)

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
    date = models.DateTimeField()
    matter = models.CharField(choices=MATTER_CHOICES, max_length=12)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('calendar entry')
        verbose_name_plural = ('calendar entries')

    def __str__(self):
        return self.matter


class Payment(BasePayment):

    def get_failure_url(self):
        return 'https://ydlearning.com/failure/'

    def get_success_url(self):
        return 'https://ydlearning.com/success/'

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                            quantity=9, price=Decimal(10), currency='USD')


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="posts")
    childs = models.ManyToManyField("Post", blank=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    text = models.CharField(max_length=4096)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:20]
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import m2m_changed

from payments import PurchasedItem
from payments.models import BasePayment


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
            print(instance.student_set.all())
            print("SEND HERE EMAIL TO ALL STUDENTS OF THE COURSE")
        print("resource has been updated")

m2m_changed.connect(resources_changed, sender=Course.resources.through)

# class PaidCourse(models.Model):


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
        return "resources/{}/{}".format(self.id, filename)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # html_template = get_template('api/verification_email.html')


        #context = {
        #    'user': self.objects user.username,
        #    'link': 'https://api.ydlearning.com/activate/{}/{}'.format(uid, token),
        #    'expires_in': str(settings.JWT_AUTH['JWT_EXPIRATION_DELTA']),
        #    'expires_time': ' hours',  # change plural!
        #    # 'logo_img_link':"",
        #    'email_sendto': user.email,
        #    'ydl_context': "Context Text",
        #    'ydl_email': "admin@ydlearning.com",
        #    'ydl_url': "https://www.ydlearning.com",
        #    'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
        #    'ydl_url_impr': "https://www.ydlearning.com/sites/impressum.html",
        #}
        #html = html_template.render(context)
#
        #send_mail(
        #    # Subject
        #    '[Y&D Learning] Please verify your email address.',
        #    '',
        #    # Content
        #    #
        #    # Email send from
        #    # 'admin@ydlearning.com',
        #    'no-reply@ydlearning.com',
        #    # Email send to
        #    [user.email],
        #    # fail silently
        #    fail_silently=False,
        #    html_message=html,
        #)    

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
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
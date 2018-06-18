from django.contrib import admin
from .models import Teacher, Student, Course, CalendarEntry, Anouncement, Resource, User

# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CalendarEntry)
admin.site.register(Anouncement)
admin.site.register(Resource)

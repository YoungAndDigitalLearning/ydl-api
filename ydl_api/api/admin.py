from django.contrib import admin
from .models import Teacher, Student, Course, CalendarEntry, Announcement, Resource, User, Language, Post, Message

class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "teacher", "is_teacher", "student", "isEmailActivated", "credit") 
    list_display_links = ("__str__", "teacher", "student") 


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CalendarEntry)
admin.site.register(Announcement)
admin.site.register(Resource)
admin.site.register(Language)
admin.site.register(Post)
admin.site.register(Message)

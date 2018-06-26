from django.contrib import admin
from .models import Teacher, Student, Course, CalendarEntry, Announcement, Resource, User, Language, Post, Message

"""Defines specific view for django admin view
"""
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "teacher", "is_teacher",
                    "student", "isEmailActivated", "credit")
    list_display_links = ("__str__", "teacher", "student")


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    list_display_links = ("__str__",)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    list_display_links = ("__str__",)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "description", "teacher",
                    "deadline", "student_count", "created", "price")
    list_display_links = ("__str__", "teacher")


class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "date", "course")
    list_display_links = ("__str__", "course")


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "author", "date")
    list_display_links = ("__str__", "author")


class ResourceAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "uploader", "uploaded",
                    "effective_from", "expires")
    list_display_links = ("__str__", "uploader")


class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__",)
    list_display_links = ("__str__",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "author", "date", "course")
    list_display_links = ("__str__", "author", "course")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "sender", "receiver", "text", "date")
    list_display_links = ("__str__", "sender", "receiver")


"""Models to be displayed
"""
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CalendarEntry, CalendarEntryAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)

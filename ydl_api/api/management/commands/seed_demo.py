"""Create idempotent, fictional data for local portfolio screenshots.

Run only against an isolated local development database.
"""
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from api.models import (
    Announcement, CalendarEntry, Course, Language, Message,
    Post, Student, Teacher, User,
)


def demo_datetime(year, month, day, hour=0, minute=0):
    return timezone.make_aware(
        datetime(year, month, day, hour, minute), timezone.get_current_timezone()
    )


class Command(BaseCommand):
    help = "Seed a local database with fictional, repeatable YDL demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-passwords", action="store_true",
            help="Update passwords for existing demo users as well as newly created ones.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG or os.environ.get("ENABLE_DEMO_SEED") != "1":
            raise CommandError(
                "Refusing to seed: requires DJANGO_DEBUG=1 and ENABLE_DEMO_SEED=1."
            )

        password = os.environ.get("DEMO_PASSWORD")
        if not password or len(password) < 12:
            raise CommandError("Set DEMO_PASSWORD to a local password of at least 12 characters.")

        # Avoid User.save() on an already student/teacher-flagged user:
        # the legacy User.save() method always creates related role records.
        def demo_user(username, first_name, last_name, is_student, is_teacher):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": username + "@example.invalid",
                    "is_active": True,
                },
            )
            updates = {
                "first_name": first_name,
                "last_name": last_name,
                "email": username + "@example.invalid",
                "is_student": is_student,
                "is_teacher": is_teacher,
                "isEmailActivated": True,
                "is_active": True,
            }
            if created or options["reset_passwords"]:
                updates["password"] = make_password(password)
            User.objects.filter(pk=user.pk).update(**updates)
            if is_student:
                Student.objects.get_or_create(user=user)
            if is_teacher:
                Teacher.objects.get_or_create(user=user)
            return user

        teacher = demo_user("demo_teacher", "Alex", "Morgan", False, True)
        student = demo_user("demo_student", "Sam", "Taylor", True, False)
        guest = demo_user("demo_learner", "Jamie", "Rivera", True, False)
        teacher_role = Teacher.objects.get(user=teacher)
        student_role = Student.objects.get(user=student)
        guest_role = Student.objects.get(user=guest)

        for name in ("German", "English", "Spanish", "French"):
            Language.objects.get_or_create(name=name)

        course_data = [
            ("German Conversation A2", "Practice speaking German in everyday situations.", 0, 14),
            ("Introduction to Spanish", "Vocabulary and grammar for first-time learners.", 0, 12),
            ("Intercultural Communication", "Explore communication across cultures.", 15, 9),
        ]
        courses = []
        for index, (name, description, price, count) in enumerate(course_data):
            course, _ = Course.objects.update_or_create(
                name=name,
                teacher=teacher_role,
                defaults={
                    "description": description,
                    "deadline": demo_datetime(2027, 6, 30),
                    "price": price,
                    "student_count": count,
                },
            )
            courses.append(course)
        student_role.courses.add(courses[0], courses[1])
        guest_role.courses.add(courses[1])

        announcements = [
            ("Welcome to Young & Digital Learning", "Discover languages and exchange ideas with fellow learners."),
            ("New semester courses", "Our new demonstration course catalogue is now available."),
        ]
        for title, content in announcements:
            Announcement.objects.update_or_create(
                title=title, author=teacher, defaults={"content": content}
            )

        for course, subject, when in [
            (courses[0], "HOMEWORK", demo_datetime(2027, 3, 8, 15, 0)),
            (courses[0], "PRESENTATION", demo_datetime(2027, 3, 15, 14, 0)),
            (courses[1], "EXAM", demo_datetime(2027, 4, 12, 10, 0)),
        ]:
            CalendarEntry.objects.get_or_create(
                course=course, matter=subject, date=when
            )

        Post.objects.update_or_create(
            course=courses[0], author=teacher, title="Course introduction",
            defaults={"text": "Welcome! Introduce yourself and share your learning goals."},
        )
        Message.objects.get_or_create(
            sender=teacher, receiver=student,
            text="Welcome to your German conversation course!",
        )

        self.stdout.write(self.style.SUCCESS(
            "Demo data ready: 3 fictional users, 3 courses, 2 announcements, "
            "3 calendar entries, 1 forum post and 1 message."
        ))
        self.stdout.write(
            "Login: demo_student or demo_teacher (password from DEMO_PASSWORD)."
        )

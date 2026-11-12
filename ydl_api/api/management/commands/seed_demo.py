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

        # Remove only the exact placeholder created by our previous seeder.
        Post.objects.filter(
            course=courses[0], author=teacher,
            title="Course introduction",
            text="Welcome! Introduce yourself and share your learning goals."
        ).delete()

        # Forum: three realistic top-level discussions and two replies.
        # update_or_create ensures repeatable data without duplicates.
        discussions = [
            (courses[0], teacher, "Welcome to German Conversation A2",
             "Welcome to the course! Each week we will practise speaking through "
             "everyday situations. Please introduce yourself and tell us one "
             "conversation topic you would like to explore."),
            (courses[0], student, "Preparing for our next speaking session",
             "For next week's session, please prepare a short introduction "
             "to a place you enjoy visiting. We will use these examples "
             "to practise asking follow-up questions in German."),
            (courses[1], teacher, "Spanish A1: learning resources and vocabulary",
             "Our first vocabulary set covers greetings, introductions and "
             "common expressions. Review the examples before the next class "
             "and share a useful phrase you have learned."),
        ]
        roots = []
        for course, author, title, body in discussions:
            post, _ = Post.objects.update_or_create(
                course=course, author=author, title=title,
                defaults={"text": body}
            )
            roots.append(post)

        replies = [
            (roots[0], student, "My learning goals",
             "Hi everyone! I would like to become more confident "
             "speaking German at university and in everyday conversations."),
            (roots[0], teacher, "A good starting point",
             "Great goal! We will start with introductions and "
             "short role-playing exercises."),
            (roots[1], guest, "My presentation topic",
             "I will prepare a short presentation about my favourite "
             "park and why I enjoy spending time there."),
        ]
        for root, author, title, body in replies:
            reply, _ = Post.objects.update_or_create(
                course=root.course, author=author, title=title,
                defaults={"text": body}
            )
            root.childs.add(reply)

        # A quiz to back the legacy frontend's GET /quiz/tests/1 call.
        # Note: in a nonempty database this may not have primary key 1.
        from quiz.models import Test, Task, Answer
        quiz, _ = Test.objects.get_or_create(
            course=courses[0], t_id=1,
            defaults={"scored_by": student}
        )
        question, _ = Task.objects.get_or_create(
            test=quiz, question="Which phrase is a polite greeting in German?",
            defaults={"render_type": "MC"}
        )
        for order, (text, score) in enumerate([
            ("Guten Morgen", 1), ("Auf Wiedersehen", 0),
            ("Gute Nacht", 0)
        ], start=1):
            Answer.objects.update_or_create(
                task=question, answer=text,
                defaults={
                    "checked": False,
                    "correct_answer": "Guten Morgen",
                    "max_score": score,
                    "score": 0,
                    "order": order,
                }
            )

        Message.objects.get_or_create(
            sender=teacher, receiver=student,
            text="Welcome to your German conversation course!",
        )

        self.stdout.write(self.style.SUCCESS(
            "Demo data ready: 3 fictional users, 3 courses, 2 announcements, "
            "3 calendar entries, 3 forum threads, 3 replies, 1 quiz and 1 message."
        ))
        self.stdout.write(
            "Login: demo_student or demo_teacher (password from DEMO_PASSWORD)."
        )

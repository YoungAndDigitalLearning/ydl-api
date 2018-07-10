from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsTeacherOrHasAuthority(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        has_authority = False
        courses_with_resource_and_student = obj.course_set.filter(student=request.user.student).count()
        print("cou", courses_with_resource_and_student)
        if courses_with_resource_and_student > 0:
            has_authority = True

        if request.user.is_teacher or has_authority:
            return True
        raise PermissionDenied({"message":"You dont have permission to acces", "object_id":obj.id})
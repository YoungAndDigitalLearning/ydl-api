from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsTeacherOrHasAuthority(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        has_authority = False
        irgendwas = obj.course_set.filter(user=request.user)
        print("is", irgendwas)

        if request.user.is_teacher or has_authority:
            return True
        raise PermissionDenied({"message":"You dont have permission to acces", "object_id":obj.id})
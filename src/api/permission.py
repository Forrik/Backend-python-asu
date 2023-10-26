from rest_framework.permissions import BasePermission

from api.constants import Role


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, "role"):
            return False
        if request.user.role is None:
            return False
        if request.user.role == Role.STUDENT.value:
            return True
        return False


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, "role"):
            return False
        if request.user.role is None:
            return False
        if request.user.role == Role.TEACHER.value:
            return True
        return False


class IsSpecialist(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, "role"):
            return False
        if request.user.role is None:
            return False
        if request.user.role == Role.SPECIALIST.value:
            return True
        return False


class IsSpecialistOrTeacher(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, "role"):
            return False
        if request.user.role is None:
            return False
        if (
            request.user.role == Role.SPECIALIST.value
            or request.user.role == Role.TEACHER.value
        ):
            return True
        return False


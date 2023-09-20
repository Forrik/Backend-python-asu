from rest_framework.permissions import BasePermission
from api.constants import Role

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'role'):
            return False
        if request.user.role is None: 
            return False
        if request.user.role == Role.STUDENT.value:
            return True
        return False

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.name == "Преподаватель":
            return True
        return False

class IsSpecialist(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.name == "Специалист УМР":
            return True
        return False
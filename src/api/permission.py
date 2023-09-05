from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.name == "Студент":
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
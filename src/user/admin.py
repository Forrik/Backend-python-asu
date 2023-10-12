from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "is_staff",
        "academic_title",
        "academic_degree",
        "education_base",
        "student_status",
        "student_group",
        "position",
        "speciality",
        "education_level",
        "number_student_book",
        "role"
        
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональные данные",
            {"fields": ("first_name", "last_name", "middle_name", "email")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Должность", {"fields": ("position",)}),
        ("Ученое звание(для преподавателя)", {"fields": ("academic_title",)}),
        ("Ученая степень (для преподавателя)", {"fields": ("academic_degree",)}),
        ("Основа обучения", {"fields": ("education_base",)}),
        ("Статус (для студента)", {"fields": ("student_status",)}),
        ("Группа (для студента)", {"fields": ("student_group",)}),
        ("Специальность", {"fields": ("speciality",)}),
        ("Образование", {"fields": ("education_level",)}),
        ("Зачетная книжка", {"fields": ("number_student_book",)}),
        ("Роль", {"fields": ("role",)}),
    )


admin.site.register(User, CustomUserAdmin)

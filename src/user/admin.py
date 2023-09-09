from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'middle_name', 'last_name',  'is_staff',
        'role', 'academicTitle', 'academicDegree', 'educationBase', 'studStatus', 'studentGroup', 'position', 'speciality', 'eduLevel', 'number_student_book'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'middle_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),

        ('Position', {
            'fields': ('position',)
        }),
        ('Role', {
            'fields': ('role',)
        }),
        ('academicTitle', {
            'fields': ('academicTitle',)
        }),
        ('academicDegree', {
            'fields': ('academicDegree',)
        }),
        ('educationBase', {
            'fields': ('educationBase',)
        }),
        ('studStatus', {
            'fields': ('studStatus',)
        }),
        ('studentGroup', {
            'fields': ('studentGroup',)
        }),
        ('speciality', {
            'fields': ('speciality',)
        }),
        ('eduLevel', {
            'fields': ('eduLevel',)
        }),
        ('number_student_book', {
            'fields': ('number_student_book',)
        })

    )

admin.site.register(User, CustomUserAdmin)
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import Role
from api.models import (AcademicDegree, AcademicTitle, EducationBase,
                        EducationLevel, Position, Speciality, StudentGroup,
                        StudentStatus, VkrHours)


class User(AbstractUser):
    middle_name = models.CharField(verbose_name="Отчество", max_length=128, blank=True)
    about = models.TextField(
        blank=True, max_length=1024, verbose_name="Информация о пользователе"
    )
    number_student_book = models.IntegerField(
        blank=True, null=True, verbose_name="Номер зачетной книжки"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Должность",
    )
    academic_title = models.ForeignKey(
        AcademicTitle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ученое звание",
    )
    academic_degree = models.ForeignKey(
        AcademicDegree,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ученая степень",
    )

    role = models.IntegerField(
        choices=[
            (Role.STUDENT.value, "Студент"),
            (Role.TEACHER.value, "Преподаватель"),
            (Role.SPECIALIST.value, "Специалист УМР"),
        ],
        default=None,
        null=True,
        verbose_name="Роль",
    )

    education_base = models.ForeignKey(
        EducationBase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Основа обучения",
    )
    student_status = models.ForeignKey(
        StudentStatus,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Статус студента",
        blank=True,
    )
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Группа",
        related_name="student_group",
        blank=True,
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Специальность",
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Уровень образования",
    )


from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models import Position, AcademicTitle, AcademicDegree, EducationBase, StudStatus, StudentGroup, Speciality, EduLevel, VkrHours

from api.constants import Role

class User(AbstractUser):
    #custom_field = models.BooleanField(default=False)
    middle_name = models.CharField(verbose_name='Отчество', max_length=128, blank=True)
    about = models.TextField(blank=True, max_length=1024)
    number_student_book = models.IntegerField(blank=True, null=True)
    position = models.ForeignKey(Position,  on_delete=models.SET_NULL, null=True, blank=True)
    academicTitle = models.ForeignKey(AcademicTitle,  on_delete=models.SET_NULL, null=True,  blank=True,)
    academicDegree = models.ForeignKey(AcademicDegree,  on_delete=models.SET_NULL, null=True,  blank=True, verbose_name='Ученая степень')

    role = models.IntegerField(
        choices=[
            (Role.STUDENT.value, "Студент"),
            (Role.TEACHER.value, "Преподаватель"),
            (Role.SPECIALIST.value, "Специалист УМР"),
        ], default=None, null=True, verbose_name='Роль')


    educationBase = models.ForeignKey(EducationBase,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Основа обучения')
    studStatus = models.ForeignKey(StudStatus,  on_delete=models.SET_NULL, null=True, verbose_name='Статус студента', blank=True)
    studentGroup = models.ForeignKey(StudentGroup,  on_delete=models.SET_NULL, null=True, verbose_name='Группа', related_name='student_group', blank=True)
    speciality = models.ForeignKey(Speciality,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Специальность')
    eduLevel = models.ForeignKey(EduLevel,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Уровень образования')
    vkrHours = models.ForeignKey(VkrHours,  on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name='Часы на ВКР')

   
    

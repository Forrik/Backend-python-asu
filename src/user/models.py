from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models import Role, Position, AcademicTitle, AcademicDegree, EducationBase, StudStatus, StudentGroup

class User(AbstractUser):
    #custom_field = models.BooleanField(default=False)
    middle_name = models.CharField(verbose_name='Отчество', max_length=128, blank=True)
    about = models.TextField(blank=True, max_length=1024)
    number_student_book = models.IntegerField(blank=True, null=True)
    position = models.ForeignKey(Position,  on_delete=models.SET_NULL, null=True, blank=True)
    academicTitle = models.ForeignKey(AcademicTitle,  on_delete=models.SET_NULL, null=True)
    academicDegree = models.ForeignKey(AcademicDegree,  on_delete=models.SET_NULL, null=True, verbose_name='Ученая степень')
    role = models.ForeignKey(Role,  on_delete=models.SET_NULL, null=True,)
    educationBase = models.ForeignKey(EducationBase,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Основа обучения')
    studStatus = models.ForeignKey(StudStatus,  on_delete=models.SET_NULL, null=True, verbose_name='Статус студента', blank=True)
    studentGroup = models.ForeignKey(StudentGroup,  on_delete=models.SET_NULL, null=True, verbose_name='Группа', blank=True)
    
   
    

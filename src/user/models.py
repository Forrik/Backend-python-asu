from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.db import models

from api.constants import Role
from api.models import (AcademicDegree, AcademicTitle, Consultancy, ConsultancyType, EducationBase,
                        EducationLevel, Position, Speciality, StudentGroup,
                        StudentStatus, Ticket, TimeNorm)
from django.contrib.auth import password_validation
from api.constants import TicketStatusEnum
from api.exceptions import BussinesLogicException
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class CustomManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        # email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

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
    
    password_text = models.CharField(max_length=128, blank=True, null=True)
    
    objects = CustomManager()

    
    def get_abbreviation(self):
        _first_name = self.first_name[:1]+'.' if self.first_name else ''
        _middle_name = self.middle_name[:1]+'.' if self.middle_name else ''
        return f"{self.last_name} {_first_name} {_middle_name}"

    def get_used_hours(self, graduation):
        '''
        Количество занятых часов в контексте заданного выпуска
        '''
        tickets_qs = Ticket.objects.filter(
            student__student_group__graduation=graduation,
            ticket_status=TicketStatusEnum.ACCEPTED.value,
            teacher=self
        ).select_related(
            "student__student_group__speciality"
            )
        try:
            main_con_type = ConsultancyType.objects.filter(is_main=True).get()
            main_con_type_id = main_con_type.id
        except ObjectDoesNotExist:
            raise BussinesLogicException(details="Не задан основной тип консультации")
        
        except MultipleObjectsReturned:
            raise BussinesLogicException(details="Задано несколько основных типов консультации")

    
        cons_qs = Consultancy.objects.filter(
            student__student_group__graduation=graduation,
            teacher=self
        ).select_related(
            "student__student_group__speciality",
            "consultancy_type")

        spec_ids = set(tickets_qs.values_list(
            "student__student_group__speciality__id", flat=True
        ).union(cons_qs.values_list("student__student_group__speciality__id", flat=True)))
        
        timenorms = TimeNorm.objects.filter(
            speciality__id__in=spec_ids
        ).values(
            "consultancy_type",
            "speciality",
            "graduation",
            "hours")

        tn_dict = {}
        for tn in timenorms:
            tn_dict[f"{tn['consultancy_type']}_{tn['speciality']}_{tn['graduation']}"] = tn['hours']

        hours = 0

        for ticket in tickets_qs:
            _hours = tn_dict.get(f"{main_con_type_id}_{ticket.student.student_group.speciality.id}_{graduation.id}")
            if _hours is None:
                    err_text = (f"Не задана норма времени для специальности "
                                f"`{ticket.student.student_group.speciality}`,выпуска `{graduation.id}` "
                                f"и типа  консультации `{main_con_type}`")

                    raise BussinesLogicException(details=err_text)
            hours += _hours

        for consultancy in cons_qs:
            _cons_hours = tn_dict.get(f"{consultancy.consultancy_type.id}_{consultancy.student.student_group.speciality.id}_{graduation.id}")

            if _cons_hours is None:
                err_text = (f"Не задана норма времени для специальности "
                            f"`{consultancy.stident.student_group.speciality}`,выпуска `{graduation.id}` "
                            f"и типа  консультации `{consultancy.consultancy_type}`")
                raise BussinesLogicException(details=err_text)
            
            hours += _cons_hours
        return hours

    
    def save(self, *args, **kwargs):
        if self._password is not None:
            self.password_text = self._password

        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)

            self._password = None
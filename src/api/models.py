from django.db import models

from api.constants import TicketStatusEnum
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from api.constants import Role
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from api.exceptions import BussinesLogicException

class Position(models.Model):
    """
    Должность
    """

    name = models.CharField(
        verbose_name="Название должности",
        blank=False,
        null=False,
        max_length=128,
        unique=True,
    )

    class Meta:
        ordering = ["-id"]
        db_table = "positions"
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return f"{self.id}: {self.name}"


class Ticket(models.Model):
    dt_send = models.DateTimeField(
        verbose_name="Дата отправки заявки", blank=False, null=False, auto_now_add=True
    )
 
    comment = models.CharField(
        verbose_name="Комментарий", blank=True, null=True, max_length=1024
    )

    ticket_status = models.IntegerField(
        choices=[
            (TicketStatusEnum.NEW.value, TicketStatusEnum.NEW.descr),
            (TicketStatusEnum.ACCEPTED.value, TicketStatusEnum.ACCEPTED.descr),
            (TicketStatusEnum.REJECTED.value, TicketStatusEnum.REJECTED.descr),
        ],
        default=TicketStatusEnum.NEW.value,
        verbose_name="Статус заявки",
    )
    teacher = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="teacher"
    )
    student = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="student"
    )
    dt_response = models.DateTimeField(
        verbose_name="Дата ответа", blank=True, null=True
    )

    _validation_error_text = f"Не удалось создать заявку. Обратитесь к администратору системы. Детали:"
    
    def __check_free_hours(self):
        student_group = self.student.student_group
        if student_group is None:
            raise ValidationError(message=  f"Для студента {self.student} (id={self.student.id}) не задана учебная группа")
        
        used_hours = self.teacher.get_used_hours(student_group.graduation)
        try:
            all_hours = VkrHours.objects.get(teacher=self.teacher, year=student_group.graduation.year).hours
        except ObjectDoesNotExist:
            raise ValidationError(message=  f"Для преподавателя {self.teacher.get_abbreviation()} (id={self.teacher.id}) не задано количество часов для ВКР")
        
        except MultipleObjectsReturned:
            raise ValidationError(message = f"Для преподавателя {self.teacher.get_abbreviation()} (id={self.teacher.id}) существует более одной записи с количеством часов для ВКР")
        try:
            main_consultancy_type = ConsultancyType.objects.filter(is_main=True).get()

        except ObjectDoesNotExist:
            raise ValidationError(message="Не задан основной тип консультации")
        
        except MultipleObjectsReturned:
            raise ValidationError(message="Задано несколько основных типов консультации")
        try:
            hours_for_ticket = TimeNorm.objects.get(
                graduation=student_group.graduation,
                speciality=student_group.speciality,
                consultancy_type=main_consultancy_type,
                )
        except ObjectDoesNotExist:
            raise ValidationError(message="Не задана норма времени для основного типа консультации")
        
        except MultipleObjectsReturned:
            raise ValidationError(message="Задано несколько норм времени для основного типа консультации")


        hours_delta = all_hours - used_hours - hours_for_ticket.hours
        if hours_delta <= 0:
            raise ValidationError(
                f"Невозможно сформировать заявку, т.к. у преподавателя {self.teacher.get_abbreviation()} не осталось свободных часов")
        return True

    def clean_fields(self, *args, **kwargs):
        super().clean_fields(*args, **kwargs)
        
        if self.student.role != Role.STUDENT.value:
            raise ValidationError(f"{self._validation_error_text} Пользователь {self.student.get_abbreviation()} (id={self.student.id}) не является студентом") 
        
        if self.teacher.role != Role.TEACHER.value:
            raise ValidationError(f"{self._validation_error_text} Пользователь {self.teacher.get_abbreviation()} (id={self.teacher.id}) не является преподавателем")
        
        is_new_ticket = True if self.id == None else False

        # Если уже есть ACCEPTED заявка, то все остальные отклоняются
        if is_new_ticket:
            if Ticket.objects.filter(
                student=self.student,
                ticket_status=TicketStatusEnum.ACCEPTED.value
            ).exists():
                raise ValidationError(f"Уже существует принятая заявка")
        else:
            existed_ticket = Ticket.objects.get(id=self.id)

            # если статус заявки меняется
            if existed_ticket.ticket_status != self.ticket_status and self.ticket_status == TicketStatusEnum.ACCEPTED:
                if Ticket.objects.filter(
                    student=self.student,
                    ticket_status=TicketStatusEnum.ACCEPTED.value
                ).exists():
                    raise ValidationError(f"Уже существует принятая заявка")

        if self.ticket_status in [TicketStatusEnum.ACCEPTED.value, TicketStatusEnum.NEW.value]:
            self.__check_free_hours()

        

        

    def save(self, *args, **kwargs):
        self.clean_fields()

        # Если заявка меняет статус на ACCEPTED, то все остальные заявки становятся REJECTED
        if self.ticket_status == TicketStatusEnum.ACCEPTED.value:
            Ticket.objects \
            .filter(student=self.student) \
            .exclude(student=self.student, teacher=self.teacher) \
            .update(ticket_status=TicketStatusEnum.REJECTED.value)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]
        db_table = "ticket"
        verbose_name = "заявка"
        verbose_name_plural = "заявки"

        constraints = [
            UniqueConstraint(
                'teacher',
                'student',
                name='ticket_teacher_student_unique',
                violation_error_message='Заявка уже существует',
            ),
        ]

    def __str__(self):
        return f"Заявка на консультацию №{self.id} от {self.student} к {self.teacher}"


class AcademicTitle(models.Model):
    """
    Ученое звание
    """

    name = models.CharField(
        verbose_name="Название ученого звания", blank=False, null=False, max_length=128, unique=True
    )
    abbreviation = models.CharField(
        verbose_name="Сокращенное название ученого звания",
        default="аббревиатура",
        max_length=128, 
    )

    class Meta:
        ordering = ["-id"]
        db_table = "academic_title"
        verbose_name = "Ученое звание"
        verbose_name_plural = "Ученые звания"

    def __str__(self):
        return f"{self.id}: {self.name}"


class AcademicDegree(models.Model):
    """
    Ученая степень
    """

    name = models.CharField(
        verbose_name="Название ученой степени", blank=False, null=False, max_length=128, unique=True
    )
    abbreviation = models.CharField(
        verbose_name="Сокращенное название ученой степени",
        default="аббревиатура",
        max_length=128,
    )

    class Meta:
        ordering = ["-id"]
        db_table = "academic_degree"
        verbose_name = "Ученая степень"
        verbose_name_plural = "Ученые степени"

    def __str__(self):
        return f"{self.id}: {self.name}"


class EducationBase(models.Model):
    """
    Основа обучения (бюджет, договор, целевая квота)
    """

    name = models.CharField(
        verbose_name="Название основы обучения", blank=False, null=False, max_length=128, unique=True
    )

    class Meta:
        ordering = ["-id"]
        db_table = "education_base"
        verbose_name = "Основа обучения"
        verbose_name_plural = "Основы обучения"

    def __str__(self):
        return f"{self.id}: {self.name}"


class VkrHours(models.Model):
    """
    Количество часов на ВКР для преподавателя
    """

    year = models.IntegerField(verbose_name="Год", blank=False, null=False)
    hours = models.IntegerField(verbose_name="Часы", blank=False, null=False)
    teacher = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, null=False, related_name="user"
    )

    class Meta:
        ordering = ["-id"]
        db_table = "vkr_hours"
        verbose_name = "Часы на ВКР"
        verbose_name_plural = "Часы на ВКР"

        constraints = [
            UniqueConstraint(
                'year',
                'teacher',
                name='vkrhours_year_teacher_unique',
                violation_error_message='Часы на ВКР для этого преподавателя и года уже заданы',
            ),
        ]

    def __str__(self):
        return f"{self.teacher.id}:" + str(self.hours) + " часов" + " " + str(self.year)


class StudentStatus(models.Model):  # TODO ?? какие статусы быват у студентов?
    """
    Статус студента
    """

    name = models.CharField(
        verbose_name="Статус студента", blank=False, null=False, max_length=128
    )

    class Meta:
        ordering = ["-id"]
        db_table = "student_status"
        verbose_name = "Статус студента"
        verbose_name_plural = "Статусы студентов"

    def __str__(self):
        return f"{self.id}: {self.name}"


class ConsultancyType(models.Model):
    """
    Тип консультации
    """

    name = models.CharField(
        verbose_name="Тип консультации", blank=False, null=False, max_length=128, unique=True
    )
    is_main = models.BooleanField(
        verbose_name="Основной", blank=False, null=False, default=False
    )

    class Meta:
        ordering = ["-id"]
        db_table = "consultancy_type"
        verbose_name = "Вид работы"
        verbose_name_plural = "Вид консультации"

    def __str__(self):
        return f"{self.id}: {self.name}"


class Consultancy(models.Model):

    consultancy_type = models.ForeignKey(
        ConsultancyType, on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, null=False, related_name="teacherr"
    )
    student = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, null=False, related_name="studentt"
    )
    comment = models.CharField(
        verbose_name="Комментарий", blank=True, null=True, max_length=512
    )
    _validation_error_text = f"Не удалось создать заявку. Обратитесь к администратору системы. Детали:"
    def __check_free_hours(self):
        student_group = self.student.student_group
        used_hours = self.teacher.get_used_hours(student_group.graduation)
        try:
            all_hours = VkrHours.objects.get(teacher=self.teacher, year=student_group.graduation.year).hours
        except ObjectDoesNotExist:
            raise ValidationError(message = f"Для преподавателя {self.teacher.get_abbreviation()} (id={self.teacher.id}) не задано количество часов для ВКР")
        
        except MultipleObjectsReturned:
            raise ValidationError(message = f"Для преподавателя {self.teacher.get_abbreviation()} (id={self.teacher.id}) существует более одной записи с количеством часов для ВКР")

        try:
            hours_for_ticket = TimeNorm.objects.get(
                graduation=student_group.graduation,
                speciality=student_group.speciality,
                consultancy_type=self.consultancy_type,
                )
        except ObjectDoesNotExist:
            raise ValidationError(message="Не задана норма времени для выбранного типа консультации")
        
        except MultipleObjectsReturned:
            raise ValidationError(message="Задано несколько норм времени для выбранного типа консультации")


        hours_delta = all_hours - used_hours - hours_for_ticket.hours
        if hours_delta <= 0:
            raise ValidationError(
                f"Невозможно выполнить запись на консультацию, т.к. у преподавателя {self.teacher.get_abbreviation()} не осталось свободных часов")
        return True

    def clean_fields(self, *args, **kwargs):
        super().clean_fields(*args, **kwargs)
        
        if self.student.role != Role.STUDENT.value:
            raise ValidationError(f"{self._validation_error_text} Пользователь {self.student.get_abbreviation()} (id={self.student.id}) не является студентом") 
        
        if self.teacher.role != Role.TEACHER.value:
            raise ValidationError(f"{self._validation_error_text} Пользователь {self.teacher.get_abbreviation()} (id={self.teacher.id}) не является преподавателем")

        self.__check_free_hours()
        

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]
        db_table = "consultancy"
        verbose_name = "Консультирование"
        verbose_name_plural = "Консультирования"

        constraints = [
            UniqueConstraint(
                'teacher',
                'student',
                'consultancy_type',
                name='consultancy_teacher_student_unique',
                violation_error_message='Консультация уже существует',
            ),
        ]

    def __str__(self):
        return f"{self.id}: {self.teacher} к {self.student}"


class EducationLevel(models.Model):
    """
    Уровень образования
    """

    name = models.CharField(
        verbose_name="Уровень образования", blank=False, null=False, max_length=128, unique=True
    )

    class Meta:
        ordering = ["-id"]
        db_table = "edu_level"
        verbose_name = "Уровень образования"
        verbose_name_plural = "Уровни образования"

    def __str__(self):
        return f"{self.id}: {self.name}"


class EducationForm(models.Model):
    """
    Форма обучения
    """

    name = models.CharField(
        verbose_name="Название формы обучения", blank=False, null=False, max_length=128, unique=True
    )

    class Meta:
        ordering = ["-id"]
        db_table = "edu_form"
        verbose_name = "Форма обучения"
        verbose_name_plural = "Формы обучения"
        

    def __str__(self):
        return f"{self.id}: {self.name}"
    


class Graduation(models.Model):
    """
    Выпуск
    """

    graduation_type = models.CharField(
        verbose_name="Тип выпуска", blank=False, null=False, max_length=128
    )
    year = models.IntegerField(verbose_name="Год", blank=False, null=False)

    class Meta:
        ordering = ["-id"]
        db_table = "graduation"
        verbose_name = "Выпуск"
        verbose_name_plural = "Выпуски"

        constraints = [
            UniqueConstraint(
                'graduation_type',
                'year',
                name='graduation_type_unique',
                violation_error_message='Такой выпуск уже существует',
            ),
        ] 

    def __str__(self):
        return f"id: {self.id}"


class Speciality(models.Model):

    code = models.CharField(
        verbose_name="Код специальности", blank=False, null=False, max_length=128
    )
    name = models.CharField(
        verbose_name="Название специальности", blank=False, null=False, max_length=128
    )
    abbreviation = models.CharField(
        verbose_name="Сокращенное название специальности",
        blank=False,
        null=False,
        max_length=128,
    )
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True, verbose_name='Уровень образования')

    class Meta:
        ordering = ["-id"]
        db_table = "speciality"
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

        

    def __str__(self):
        return f"Специльность №{self.id} {self.name}"
    


class StudentGroup(models.Model):
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Специальность"
    )
    course = models.IntegerField(verbose_name="Курс", blank=False, null=False)
    number = models.IntegerField(verbose_name="Номер группы", blank=False, null=False)
    education_form = models.ForeignKey(
        EducationForm,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Форма образования",
    )
    graduation = models.ForeignKey(
        Graduation, on_delete=models.SET_NULL, null=True, verbose_name="Выпуск"
    )

    class Meta:
        ordering = ["-id"]
        db_table = "student_group"
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

        constraints = [
            UniqueConstraint(
                'speciality',
                'course',
                'number',
                'graduation',
                'education_form',
                name='student_group_unique',
                violation_error_message='Группа уже существует',
            ),
        ]

    def __str__(self):
        if self.speciality:
            return f"{self.speciality.abbreviation}-{self.course}{self.number}"
        return f"У группы не указана аббревиатура"

    


class TimeNorm(models.Model):
    """
    Определяет норму времени для консультации определенного вида,
    определенной группы, определенного выпуска
    """

    hours = models.IntegerField(
        verbose_name="Количество часов", blank=False, null=False
    )
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Специальность"
    )
    consultancy_type = models.ForeignKey(
        ConsultancyType,
        on_delete=models.CASCADE,
        blank=False, null=False,
        verbose_name="Вид консультации",
    )
    graduation = models.ForeignKey(
        Graduation, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Выпуск"
    )

    class Meta:
        ordering = ["-id"]
        db_table = "time_norm"
        verbose_name = "Норма времени"
        verbose_name_plural = "Нормы времени"

        constraints = [
            UniqueConstraint(
                'speciality',
                'graduation',
                'consultancy_type',
                name='timenorm_for_speciality_graduation_consultancy_unique',
                violation_error_message='Норма времени уже существует',
            ),
        ]
    


    def __str__(self):
        return f"Норма для {self.speciality}: ({self.consultancy_type})"

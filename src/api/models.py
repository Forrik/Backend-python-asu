
from django.db import models


class Role(models.Model):
    name = models.CharField(verbose_name='Название роли',
                            blank=False,  null=False, max_length=128, unique=True)

    class Meta:
        ordering = ['-id']
        db_table = 'roles'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return f'{self.id}: {self.name}'


class Position(models.Model):
    name = models.CharField(verbose_name='Название должности',
                            blank=False, null=False, max_length=128, unique=True)

    class Meta:
        ordering = ['-id']
        db_table = 'positions'
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return f'{self.id}: {self.name}'


class TicketStatus(models.Model):
    name = models.CharField(verbose_name='Название статуса заявки',
                            blank=False, null=False, max_length=128, unique=True)

    class Meta:
        ordering = ['-id']
        db_table = 'ticket_status'
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'

    def __str__(self):
        return f'{self.id}: {self.name}'


class Ticket(models.Model):
    dt_send = models.DateTimeField(
        verbose_name="Дата отправки заявки", blank=False, null=False, auto_now_add=True)
    message = models.TextField(
        verbose_name="Сообщение", blank=False, null=False, max_length=1024)
    ticketStatus = models.ForeignKey(
        TicketStatus, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, null=True, related_name='teacher')
    student = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, null=True, related_name='student')
    dt_response = models.DateTimeField(
        verbose_name="Дата ответа", blank=True, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'ticket'
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'Заявка на консультацию №{self.id} от {self.student} к {self.teacher}'


class AcademicTitle(models.Model):
    name = models.CharField(
        verbose_name='Название ученого звания',  blank=False, null=False, max_length=128)
    abbreviation = models.CharField(
        verbose_name='Сокращенное название ученого звания', default='аббревиатура', max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'academic_title'
        verbose_name = 'Ученое звание'
        verbose_name_plural = 'Ученые звания'

    def __str__(self):
        return f'{self.id}: {self.name}'


class AcademicDegree(models.Model):
    name = models.CharField(
        verbose_name='Название ученой степени', blank=False, null=False, max_length=128)
    abbreviation = models.CharField(
        verbose_name='Сокращенное название ученой степени', default='аббревиатура', max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'academic_degree'
        verbose_name = 'Ученая степень'
        verbose_name_plural = 'Ученые степени'

    def __str__(self):
        return f'{self.id}: {self.name}'


class EducationBase(models.Model):
    name = models.CharField(
        verbose_name='Название основы обучения', blank=False, null=False, max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'education_base'
        verbose_name = 'Основа обучения'
        verbose_name_plural = 'Основы обучения'

    def __str__(self):
        return f'{self.id}: {self.name}'


class VkrHours(models.Model):

    year = models.IntegerField(verbose_name='Год', blank=False, null=False)
    hours = models.IntegerField(verbose_name='Часы', blank=False, null=False)
    user_id = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'vkr_hours'
        verbose_name = 'Часы на ВКР'
        verbose_name_plural = 'Часы на ВКР'

    def __str__(self):
        return f'{self.id}:' + str(self.hours)


class StudStatus(models.Model):
    name = models.CharField(verbose_name='Статус студента',
                            blank=False, null=False, max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'student_status'
        verbose_name = 'Статус студента'
        verbose_name_plural = 'Статусы студентов'

    def __str__(self):
        return f'{self.id}: {self.name}'


class WorkType(models.Model):
    name = models.CharField(verbose_name='Вид работы',
                            blank=False, null=False, max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'work_type'
        verbose_name = 'Вид работы'
        verbose_name_plural = 'Виды работы'

    def __str__(self):
        return f'{self.id}: {self.name}'


class Consultancy(models.Model):

    workType = models.ForeignKey(
        WorkType, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, null=True, related_name='teacherr')
    student = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, null=True, related_name='studentt')
    comment = models.CharField(
        verbose_name='Комментарий', blank=False, null=False, max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'consultancy'
        verbose_name = 'Консультирование'
        verbose_name_plural = 'Консультирования'

    def __str__(self):
        return f'{self.id}: {self.teacher} к {self.student}'


class EduLevel(models.Model):

    name = models.CharField(
        verbose_name='Уровень образования', blank=False, null=False, max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'edu_level'
        verbose_name = 'Уровень образования'
        verbose_name_plural = 'Уровни образования'

    def __str__(self):
        return f'{self.id}: {self.name}'


class EduForm(models.Model):

    name = models.CharField(verbose_name='Форма обучения',
                            blank=False, null=False, max_length=128)

    class Meta:
        ordering = ['-id']
        db_table = 'edu_form'
        verbose_name = 'Форма обучения'
        verbose_name_plural = 'Формы обучения'

    def __str__(self):
        return f'{self.id}: {self.name}'


class Graduation(models.Model):

    typeGraduation = models.CharField(
    verbose_name='Тип выпуска', blank=False, null=False, max_length=128)
    year = models.IntegerField(verbose_name='Год', blank=False, null=False)

    class Meta:
        ordering = ['-id']
        db_table = 'graduation'
        verbose_name = 'Выпуск'
        verbose_name_plural = 'Выпуски'

    def __str__(self):
        return f'id: {self.id}'


class Speciality(models.Model):

    code = models.CharField(verbose_name='Код специальности',
                            blank=False, null=False, max_length=128)
    name = models.CharField(
        verbose_name='Название специальности', blank=False, null=False, max_length=128)
    abbreviation = models.CharField(
        verbose_name='Сокращенное название специальности', blank=False, null=False, max_length=128)
    edulevel = models.ForeignKey(
        EduLevel, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'speciality'
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return f'Специльность №{self.id} {self.name}'


class StudentGroup(models.Model):
    speciality_id = models.ForeignKey(
        Speciality, on_delete=models.SET_NULL, null=True)
    course = models.CharField(
        verbose_name='Курс', blank=False, null=False, max_length=128)
    number = models.IntegerField(
        verbose_name='Номер группы', blank=False, null=False)
    eduForm_id = models.ForeignKey(
        EduForm, on_delete=models.SET_NULL, null=True)
    eduGraduation_id = models.ForeignKey(
        Graduation, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'student_group'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f'{self.id}:'


class TimeNorm(models.Model):
    hours = models.IntegerField(
        verbose_name='Количество часов', blank=False, null=False)
    speciality = models.ForeignKey(
        Speciality, on_delete=models.SET_NULL, null=True)
    workType = models.ForeignKey(
        WorkType, on_delete=models.SET_NULL, null=True)
    graduation_id = models.ForeignKey(
        Graduation, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'time_norm'
        verbose_name = 'Норма времени'
        verbose_name_plural = 'Нормы времени'

    def __str__(self):
        return f'{self.id}: {self.hours} часов'

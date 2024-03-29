# Generated by Django 4.2.3 on 2023-10-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AcademicDegree",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        verbose_name="Название ученой степени",
                    ),
                ),
                (
                    "abbreviation",
                    models.CharField(
                        default="аббревиатура",
                        max_length=128,
                        verbose_name="Сокращенное название ученой степени",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ученая степень",
                "verbose_name_plural": "Ученые степени",
                "db_table": "academic_degree",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="AcademicTitle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        verbose_name="Название ученого звания",
                    ),
                ),
                (
                    "abbreviation",
                    models.CharField(
                        default="аббревиатура",
                        max_length=128,
                        verbose_name="Сокращенное название ученого звания",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ученое звание",
                "verbose_name_plural": "Ученые звания",
                "db_table": "academic_title",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Consultancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        max_length=512,
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
            ],
            options={
                "verbose_name": "Консультирование",
                "verbose_name_plural": "Консультирования",
                "db_table": "consultancy",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="ConsultancyType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Тип консультации"
                    ),
                ),
                (
                    "is_main",
                    models.BooleanField(default=False, verbose_name="Основной"),
                ),
            ],
            options={
                "verbose_name": "Вид работы",
                "verbose_name_plural": "Вид консультации",
                "db_table": "consultancy_type",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="EducationBase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        verbose_name="Название основы обучения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Основа обучения",
                "verbose_name_plural": "Основы обучения",
                "db_table": "education_base",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="EducationForm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        verbose_name="Название формы обучения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Форма обучения",
                "verbose_name_plural": "Формы обучения",
                "db_table": "edu_form",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="EducationLevel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Уровень образования"
                    ),
                ),
            ],
            options={
                "verbose_name": "Уровень образования",
                "verbose_name_plural": "Уровни образования",
                "db_table": "edu_level",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Graduation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "graduation_type",
                    models.CharField(max_length=128, verbose_name="Тип выпуска"),
                ),
                ("year", models.IntegerField(verbose_name="Год")),
            ],
            options={
                "verbose_name": "Выпуск",
                "verbose_name_plural": "Выпуски",
                "db_table": "graduation",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Название должности"
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность",
                "verbose_name_plural": "Должности",
                "db_table": "positions",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Speciality",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=128, verbose_name="Код специальности"),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, verbose_name="Название специальности"
                    ),
                ),
                (
                    "abbreviation",
                    models.CharField(
                        max_length=128,
                        verbose_name="Сокращенное название специальности",
                    ),
                ),
            ],
            options={
                "verbose_name": "Специальность",
                "verbose_name_plural": "Специальности",
                "db_table": "speciality",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="StudentGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course", models.IntegerField(verbose_name="Курс")),
                ("number", models.IntegerField(verbose_name="Номер группы")),
            ],
            options={
                "verbose_name": "Группа",
                "verbose_name_plural": "Группы",
                "db_table": "student_group",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="StudentStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, verbose_name="Статус студента"),
                ),
            ],
            options={
                "verbose_name": "Статус студента",
                "verbose_name_plural": "Статусы студентов",
                "db_table": "student_status",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dt_send",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата отправки заявки"
                    ),
                ),
                (
                    "message",
                    models.TextField(max_length=1024, verbose_name="Сообщение"),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        max_length=512,
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
                (
                    "ticket_status",
                    models.IntegerField(
                        choices=[(1, "Новая"), (2, "Принятая"), (3, "Отклонено")],
                        default=1,
                        verbose_name="Статус заявки",
                    ),
                ),
                (
                    "dt_response",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата ответа"
                    ),
                ),
            ],
            options={
                "verbose_name": "заявка",
                "verbose_name_plural": "заявки",
                "db_table": "ticket",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="TimeNorm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hours", models.IntegerField(verbose_name="Количество часов")),
            ],
            options={
                "verbose_name": "Норма времени",
                "verbose_name_plural": "Нормы времени",
                "db_table": "time_norm",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="VkrHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField(verbose_name="Год")),
                ("hours", models.IntegerField(verbose_name="Часы")),
            ],
            options={
                "verbose_name": "Часы на ВКР",
                "verbose_name_plural": "Часы на ВКР",
                "db_table": "vkr_hours",
                "ordering": ["-id"],
            },
        ),
    ]

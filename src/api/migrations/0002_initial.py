# Generated by Django 4.2.3 on 2023-10-08 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="vkrhours",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="timenorm",
            name="consultancy_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.consultancytype",
                verbose_name="Вид консультации",
            ),
        ),
        migrations.AddField(
            model_name="timenorm",
            name="graduation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.graduation",
                verbose_name="Выпуск",
            ),
        ),
        migrations.AddField(
            model_name="timenorm",
            name="speciality",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.speciality",
                verbose_name="Специальность",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="student",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="student",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teacher",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="studentgroup",
            name="education_form",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.educationform",
                verbose_name="Форма образования",
            ),
        ),
        migrations.AddField(
            model_name="studentgroup",
            name="graduation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.graduation",
                verbose_name="Выпуск",
            ),
        ),
        migrations.AddField(
            model_name="studentgroup",
            name="speciality",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.speciality",
                verbose_name="Специальность",
            ),
        ),
        migrations.AddField(
            model_name="speciality",
            name="education_level",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.educationlevel",
                verbose_name="Уровень образования",
            ),
        ),
        migrations.AddField(
            model_name="consultancy",
            name="consultancy_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.consultancytype",
            ),
        ),
        migrations.AddField(
            model_name="consultancy",
            name="student",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="studentt",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="consultancy",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teacherr",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                models.F("teacher"),
                models.F("student"),
                name="ticket_teacher_student_unique",
                violation_error_message="Заявка уже существует",
            ),
        ),
        migrations.AddConstraint(
            model_name="consultancy",
            constraint=models.UniqueConstraint(
                models.F("teacher"),
                models.F("student"),
                models.F("consultancy_type"),
                name="consultancy_teacher_student_unique",
                violation_error_message="Консультация уже существует",
            ),
        ),
    ]
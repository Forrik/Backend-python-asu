# Generated by Django 4.2.3 on 2023-09-08 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0025_rename_speciality_id_timenorm_speciality"),
        ("user", "0014_user_edulevel_alter_user_academictitle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="number_student_book",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Номер зачётной книжки"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.position",
                verbose_name="Должность",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.role",
                verbose_name="Роль",
            ),
        ),
    ]

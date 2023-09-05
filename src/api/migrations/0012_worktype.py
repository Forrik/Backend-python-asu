# Generated by Django 4.2.3 on 2023-07-18 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_studstatus_academicdegree_abbreviation_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkType",
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
                ("name", models.CharField(max_length=128, verbose_name="Вид работы")),
            ],
            options={
                "verbose_name": "Вид работы",
                "verbose_name_plural": "Виды работы",
                "db_table": "work_type",
                "ordering": ["-id"],
            },
        ),
    ]
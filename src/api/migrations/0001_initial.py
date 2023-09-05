# Generated by Django 4.2.3 on 2023-07-15 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Role",
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
                    models.CharField(max_length=128, verbose_name="Название роли"),
                ),
            ],
            options={
                "verbose_name": "Роль",
                "verbose_name_plural": "Роли",
                "db_table": "roles",
                "ordering": ["-id"],
            },
        ),
    ]

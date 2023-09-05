# Generated by Django 4.2.3 on 2023-07-18 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_alter_role_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="position",
            name="name",
            field=models.CharField(
                max_length=128, unique=True, verbose_name="Название должности"
            ),
        ),
        migrations.AlterField(
            model_name="ticketstatus",
            name="name",
            field=models.CharField(
                max_length=128, unique=True, verbose_name="Название статуса заявки"
            ),
        ),
    ]

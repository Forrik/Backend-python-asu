# Generated by Django 4.2.3 on 2023-07-18 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_timenorm"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="name",
            field=models.CharField(
                max_length=128, unique=True, verbose_name="Название роли"
            ),
        ),
    ]

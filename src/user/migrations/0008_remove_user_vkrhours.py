# Generated by Django 4.2.3 on 2023-07-18 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_user_studstatus"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="vkrHours",
        ),
    ]
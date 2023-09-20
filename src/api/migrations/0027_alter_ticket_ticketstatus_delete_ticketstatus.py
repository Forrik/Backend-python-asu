# Generated by Django 4.2.3 on 2023-09-19 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0026_alter_ticketstatus_options_alter_studentgroup_course_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="ticketStatus",
            field=models.IntegerField(
                choices=[(1, "Новая"), (2, "Принятая"), (3, "Отклонено")],
                default=1,
                verbose_name="Статус заявки",
            ),
        ),
        migrations.DeleteModel(
            name="TicketStatus",
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-19 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0030_ticketstatus_alter_ticket_ticketstatus"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TicketStatus",
        ),
    ]
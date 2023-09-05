# Generated by Django 4.2.3 on 2023-07-16 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_educationbase"),
        ("user", "0004_remove_user_ticket_remove_user_ticketstatus"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="educationBase",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.educationbase",
            ),
        ),
    ]

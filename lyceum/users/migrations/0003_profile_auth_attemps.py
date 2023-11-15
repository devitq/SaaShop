# Generated by Django 4.2.7 on 2023-11-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_customuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="auth_attemps",
            field=models.PositiveIntegerField(
                blank=True,
                default=0,
                editable=False,
                verbose_name="количество попыток входа",
            ),
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_profile_auth_attemps"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="auth_attemps",
            new_name="attempts_count",
        ),
        migrations.AddField(
            model_name="profile",
            name="blocked_timestamp",
            field=models.DateTimeField(
                null=True, verbose_name="время последней блокировки"
            ),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-05 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                    "mail",
                    models.EmailField(max_length=254, verbose_name="почта"),
                ),
                ("text", models.TextField(verbose_name="текст")),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        null=True,
                        verbose_name="дата создания",
                    ),
                ),
            ],
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-09 19:43

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "feedback",
            "0002_alter_feedback_options_feedback_name_feedback_status_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedback",
            name="mail",
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="name",
        ),
        migrations.CreateModel(
            name="PersonalData",
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
                    models.CharField(
                        blank=True,
                        max_length=1478,
                        null=True,
                        verbose_name="name_models",
                    ),
                ),
                (
                    "mail",
                    models.EmailField(
                        max_length=254, verbose_name="mail_models"
                    ),
                ),
                (
                    "feedback",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author",
                        to="feedback.feedback",
                        verbose_name="feedback_models",
                    ),
                ),
            ],
            options={
                "verbose_name": "personal_data_models",
                "verbose_name_plural": "personal_datas_models",
            },
        ),
        migrations.CreateModel(
            name="FeedbackFile",
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
                    "file",
                    models.FileField(
                        null=True,
                        upload_to=feedback.models.FeedbackFile.get_path_for_file,
                        verbose_name="file_models",
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        related_query_name="files",
                        to="feedback.feedback",
                        verbose_name="feedback_models",
                    ),
                ),
            ],
            options={
                "verbose_name": "feedback_file_models",
                "verbose_name_plural": "feedback_files_models",
            },
        ),
    ]
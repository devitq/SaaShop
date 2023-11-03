# Generated by Django 4.2.6 on 2023-11-03 13:12

import catalog.models
import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "catalog",
            "0009_category_name_en_category_name_ru_item_name_en_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "verbose_name": "category_models",
                "verbose_name_plural": "categories_models",
            },
        ),
        migrations.AlterModelOptions(
            name="item",
            options={
                "ordering": ("name", "id"),
                "verbose_name": "item_models",
                "verbose_name_plural": "items_models",
            },
        ),
        migrations.AlterModelOptions(
            name="itemimages",
            options={
                "verbose_name": "item_image_models",
                "verbose_name_plural": "item_images_models",
            },
        ),
        migrations.AlterModelOptions(
            name="mainimage",
            options={
                "verbose_name": "main_image_models",
                "verbose_name_plural": "main_images_models",
            },
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={
                "verbose_name": "tag_models",
                "verbose_name_plural": "tags_models",
            },
        ),
        migrations.AlterField(
            model_name="category",
            name="is_published",
            field=models.BooleanField(
                default=True, verbose_name="published_models"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_en",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_ru",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="a-z, 0-9, _, -",
                max_length=200,
                unique=True,
                verbose_name="slug_models",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="unique_name",
            field=models.CharField(
                editable=False,
                help_text="generated_name_for_unique",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="unique_name_models",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="weight",
            field=models.PositiveSmallIntegerField(
                default=100,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(32767),
                ],
                verbose_name="weight_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                blank=True,
                help_text="choose_category_non_required",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item",
                related_query_name="category",
                to="catalog.category",
                verbose_name="category_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                null=True,
                verbose_name="created_at_utc_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="is_on_main",
            field=models.BooleanField(
                default=False, verbose_name="show_on_main_models"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="is_published",
            field=models.BooleanField(
                default=True, verbose_name="published_models"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="main_image",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.mainimage",
                verbose_name="main_image_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name_en",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name_ru",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                help_text="choose_tags_non_required",
                related_query_name="tag",
                to="catalog.tag",
                verbose_name="tags_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=tinymce.models.HTMLField(
                help_text="text_should_contain",
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно", "perfect", "luxurious"
                    )
                ],
                verbose_name="text_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text_en",
            field=tinymce.models.HTMLField(
                help_text="text_should_contain",
                null=True,
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно", "perfect", "luxurious"
                    )
                ],
                verbose_name="text_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text_ru",
            field=tinymce.models.HTMLField(
                help_text="text_should_contain",
                null=True,
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно", "perfect", "luxurious"
                    )
                ],
                verbose_name="text_models",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="updated_at_utc_models"
            ),
        ),
        migrations.AlterField(
            model_name="itemimages",
            name="image",
            field=models.ImageField(
                null=True,
                upload_to=catalog.models.get_file_path_for_images,
                verbose_name="image_models",
            ),
        ),
        migrations.AlterField(
            model_name="itemimages",
            name="item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                related_query_name="images",
                to="catalog.item",
                verbose_name="item_models",
            ),
        ),
        migrations.AlterField(
            model_name="mainimage",
            name="main_image",
            field=models.ImageField(
                upload_to=catalog.models.get_file_path_for_main_image,
                verbose_name="image_models",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="is_published",
            field=models.BooleanField(
                default=True, verbose_name="published_models"
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name_en",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name_ru",
            field=models.CharField(
                help_text="no_more_than_150",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="title_models",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                help_text="a-z, 0-9, _, -",
                max_length=200,
                unique=True,
                verbose_name="slug_models",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="unique_name",
            field=models.CharField(
                editable=False,
                help_text="generated_name_for_unique",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="unique_name_models",
            ),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-29 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_alter_item_category_alter_item_tags_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                blank=True,
                help_text="Выберите категорию(необязательно)",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_query_name="category",
                to="catalog.category",
                verbose_name="категория",
            ),
        ),
    ]
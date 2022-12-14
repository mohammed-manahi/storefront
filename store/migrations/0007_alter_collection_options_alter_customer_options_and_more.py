# Generated by Django 4.1.2 on 2022-10-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_rename_created_at_order_placed_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={"ordering": ["title"]},
        ),
        migrations.AlterModelOptions(
            name="customer",
            options={"ordering": ["first_name", "last_name"]},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["title"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(),
        ),
    ]

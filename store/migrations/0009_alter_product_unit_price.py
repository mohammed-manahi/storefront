# Generated by Django 4.1.2 on 2022-10-30 14:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_alter_order_placed_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="unit_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]

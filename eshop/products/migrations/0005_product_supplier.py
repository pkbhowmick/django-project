# Generated by Django 5.1.1 on 2024-09-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_remove_product_supplier"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="supplier",
            field=models.CharField(default="supplier-1", max_length=255),
        ),
    ]

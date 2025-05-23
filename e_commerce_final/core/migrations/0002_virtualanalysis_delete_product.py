# Generated by Django 5.2 on 2025-05-13 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VirtualAnalysis",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="analysis/")),
                ("qr_code", models.ImageField(upload_to="analysis_qr/")),
            ],
        ),
        migrations.DeleteModel(
            name="Product",
        ),
    ]

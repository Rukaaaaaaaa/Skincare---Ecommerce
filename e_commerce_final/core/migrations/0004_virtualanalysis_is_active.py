# Generated by Django 5.2 on 2025-05-13 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_delete_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="virtualanalysis",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]

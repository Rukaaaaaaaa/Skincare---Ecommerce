# Generated by Django 5.2 on 2025-05-14 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_specialoffer_options_specialoffer_created_at_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="specialoffer",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Special Offer",
                "verbose_name_plural": "Special Offers",
            },
        ),
        migrations.AlterField(
            model_name="specialoffer",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="specialoffer",
            name="is_active",
            field=models.BooleanField(
                default=False, help_text="Đánh dấu ưu đãi đang hiển thị trên trang chủ"
            ),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-05 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookmarks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookmark",
            name="image_url",
            field=models.URLField(blank=True, null=True, verbose_name="image URL"),
        ),
    ]

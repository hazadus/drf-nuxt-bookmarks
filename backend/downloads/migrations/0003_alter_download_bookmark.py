# Generated by Django 4.1.7 on 2023-04-23 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookmarks", "0005_alter_bookmark_options"),
        ("downloads", "0002_alter_download_file_alter_download_file_size_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="download",
            name="bookmark",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="download",
                to="bookmarks.bookmark",
                verbose_name="bookmark",
            ),
        ),
    ]
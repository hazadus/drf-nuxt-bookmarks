# Generated by Django 4.1.7 on 2023-04-22 09:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bookmarks", "0004_tag_bookmark_tags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookmark",
            options={
                "ordering": [
                    "user",
                    "is_archived",
                    "-is_favorite",
                    "is_read",
                    "-created",
                ],
                "verbose_name": "bookmark",
                "verbose_name_plural": "bookmarks",
            },
        ),
    ]

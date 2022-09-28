# Generated by Django 3.2 on 2022-09-28 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="subscribe",
            constraint=models.UniqueConstraint(
                fields=("user", "author"), name="unique_user_author"
            ),
        ),
    ]

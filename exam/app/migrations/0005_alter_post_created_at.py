# Generated by Django 4.2.8 on 2023-12-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_comment_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
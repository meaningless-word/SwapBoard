# Generated by Django 5.0 on 2023-12-30 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_deleted_comment_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='rating',
        ),
    ]

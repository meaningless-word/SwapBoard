# Generated by Django 5.0 on 2023-12-28 14:52

import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryType', models.CharField(choices=[('T', 'Танки'), ('H', 'Хилы'), ('D', 'ДД'), ('S', 'Торговцы'), ('G', 'Гилдмастеры'), ('Q', 'Квестгиверы'), ('B', 'Кузнецы'), ('T', 'Кожевники'), ('P', 'Зельевары'), ('C', 'Мастера заклинаний'), ('N', 'Никто')], default='N', max_length=2)),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Заголовок')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Сообщение')),
                ('dateCreation', models.DateTimeField(auto_now_add=True)),
                ('rating', models.SmallIntegerField(default=0)),
                ('linkedAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField()),
                ('dateCreation', models.DateTimeField(auto_now_add=True)),
                ('familyTree', models.CharField(blank=True, max_length=500, null=True)),
                ('linkedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commented', to='app.comment')),
                ('linkedPost', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linkedComments', to='app.post')),
            ],
        ),
    ]

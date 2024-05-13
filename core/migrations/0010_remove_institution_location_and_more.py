# Generated by Django 5.0.4 on 2024-05-12 10:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_course_teacher'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='location',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='members',
        ),
        migrations.AddField(
            model_name='institution',
            name='telephone',
            field=models.CharField(default=0, max_length=15, unique=True, verbose_name='Telephone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='community',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-09 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_course_poster_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='poster_image',
            new_name='course_image',
        ),
    ]

# Generated by Django 5.0.4 on 2024-09-04 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_institution_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='video',
        ),
    ]

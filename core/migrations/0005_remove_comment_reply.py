# Generated by Django 5.0.4 on 2024-09-05 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_articlelike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply',
        ),
    ]
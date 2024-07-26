# Generated by Django 5.0.4 on 2024-07-25 23:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_enrollment_pending_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='pending_email',
        ),
        migrations.CreateModel(
            name='PendingEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_enrollments', to='core.course')),
            ],
        ),
    ]

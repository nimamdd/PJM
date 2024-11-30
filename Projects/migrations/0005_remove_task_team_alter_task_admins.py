# Generated by Django 5.1.2 on 2024-11-29 23:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0004_task_team'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='team',
        ),
        migrations.AlterField(
            model_name='task',
            name='admins',
            field=models.ManyToManyField(limit_choices_to={'is_admin': True}, related_name='task_admins', to=settings.AUTH_USER_MODEL),
        ),
    ]

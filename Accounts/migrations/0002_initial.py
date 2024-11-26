# Generated by Django 5.1.2 on 2024-11-25 21:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
        ('Projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='projects',
            field=models.ManyToManyField(related_name='team_projects', to='Projects.task'),
        ),
        migrations.AddField(
            model_name='profile',
            name='teams',
            field=models.ManyToManyField(blank=True, null=True, related_name='profile_teams', to='Accounts.team'),
        ),
        migrations.AddField(
            model_name='team',
            name='admin',
            field=models.ManyToManyField(blank=True, related_name='admin_team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='members_team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_team', to=settings.AUTH_USER_MODEL),
        ),
    ]

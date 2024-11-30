# Generated by Django 5.1.2 on 2024-11-29 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_remove_profile_teams_profile_team_alter_team_image'),
        ('Projects', '0003_remove_project_teams_project_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.team'),
        ),
    ]

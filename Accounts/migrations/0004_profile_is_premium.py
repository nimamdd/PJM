# Generated by Django 5.1.2 on 2024-11-28 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_alter_team_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-23 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_alter_profile_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 23, 21, 34, 5, 4803, tzinfo=datetime.timezone.utc)),
        ),
    ]

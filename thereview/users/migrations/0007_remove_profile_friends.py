# Generated by Django 4.1.7 on 2023-05-26 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friends',
        ),
    ]

# Generated by Django 4.1.7 on 2023-08-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0003_alter_playlist_medium_alter_playlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

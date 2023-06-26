# Generated by Django 4.1.7 on 2023-06-26 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0034_alter_entityactor_actor_alter_entityactor_entity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playlists', '0002_alter_playlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='medium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to='content.medium'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to=settings.AUTH_USER_MODEL),
        ),
    ]

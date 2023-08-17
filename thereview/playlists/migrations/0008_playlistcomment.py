# Generated by Django 4.1.7 on 2023-08-17 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playlists', '0007_playlist_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=999, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_comments', to='playlists.playlist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

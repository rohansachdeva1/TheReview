# Generated by Django 4.1.7 on 2023-06-26 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0034_alter_entityactor_actor_alter_entityactor_entity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_searchhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entities', models.ManyToManyField(blank=True, related_name='entities', to='content.entity')),
                ('medium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.medium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

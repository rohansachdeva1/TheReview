# Generated by Django 4.1.7 on 2023-08-15 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0041_remove_director_image'),
        ('users', '0020_profile_follows_delete_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='seen',
            field=models.ManyToManyField(blank=True, related_name='seen', to='content.entity'),
        ),
    ]

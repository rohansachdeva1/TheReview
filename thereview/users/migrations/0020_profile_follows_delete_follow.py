# Generated by Django 4.1.7 on 2023-06-29 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='users.profile'),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]

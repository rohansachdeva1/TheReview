# Generated by Django 4.1.7 on 2023-06-22 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0028_rename_description_entity_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='content_rating',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='runtime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

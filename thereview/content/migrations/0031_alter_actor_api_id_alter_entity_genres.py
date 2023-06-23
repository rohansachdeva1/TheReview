# Generated by Django 4.1.7 on 2023-06-23 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0030_rename_tag_entity_tags_remove_entity_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='api_id',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='entities', to='content.genre'),
        ),
    ]

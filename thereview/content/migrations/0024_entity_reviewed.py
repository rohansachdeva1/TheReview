# Generated by Django 4.1.7 on 2023-06-20 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_remove_entity_reviewed_remove_entity_sum_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='reviewed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

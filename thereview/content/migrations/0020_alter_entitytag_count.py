# Generated by Django 4.1.7 on 2023-06-09 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_entity_sum_scores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitytag',
            name='count',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
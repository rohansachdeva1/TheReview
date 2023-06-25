# Generated by Django 4.1.7 on 2023-06-20 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_alter_entity_overall_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='overall_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='sum_scores',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
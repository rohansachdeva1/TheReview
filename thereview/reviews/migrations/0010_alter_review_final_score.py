# Generated by Django 4.1.7 on 2023-06-06 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_alter_review_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='final_score',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2),
        ),
    ]

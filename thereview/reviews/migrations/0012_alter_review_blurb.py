# Generated by Django 4.1.7 on 2023-06-06 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_alter_review_category_rating1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='blurb',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

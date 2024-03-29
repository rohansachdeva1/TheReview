# Generated by Django 4.1.7 on 2023-08-17 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0020_reviewcomment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewcomment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to='reviews.review'),
        ),
        migrations.AlterField(
            model_name='reviewcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]

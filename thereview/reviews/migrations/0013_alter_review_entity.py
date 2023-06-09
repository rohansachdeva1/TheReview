# Generated by Django 4.1.7 on 2023-06-06 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_category_order'),
        ('reviews', '0012_alter_review_blurb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviews', to='content.entity'),
        ),
    ]

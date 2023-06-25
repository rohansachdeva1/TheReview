# Generated by Django 4.1.7 on 2023-06-22 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_remove_entity_overall_category_rating1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitytag',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.entity'),
        ),
        migrations.AlterField(
            model_name='entitytag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.tag'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-05-17 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('overall_score', models.IntegerField()),
                ('overall_rating1', models.FloatField()),
                ('overall_rating2', models.FloatField()),
                ('overall_rating3', models.FloatField()),
                ('overall_rating4', models.FloatField()),
                ('overall_rating5', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('entities', models.ManyToManyField(related_name='genreentitylinker', to='content.entity')),
                ('mediums', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.medium')),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='genres',
            field=models.ManyToManyField(related_name='genreentitylinker', to='content.genre'),
        ),
        migrations.AddField(
            model_name='entity',
            name='mediums',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.medium'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mediums', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.medium')),
            ],
        ),
    ]

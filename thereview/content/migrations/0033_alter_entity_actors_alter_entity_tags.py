# Generated by Django 4.1.7 on 2023-06-23 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0032_entity_imdbratingvotes_alter_actor_api_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='actors',
            field=models.ManyToManyField(blank=True, through='content.EntityActor', to='content.actor'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='tags',
            field=models.ManyToManyField(blank=True, through='content.EntityTag', to='content.tag'),
        ),
    ]
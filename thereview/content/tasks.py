# tasks.py
from celery import shared_task
import requests
import asyncio

from content.models import Actor, Entity, EntityActor

async def fetch_actor_info(entity_id):
    print(entity_id)
    data = requests.get('https://imdb-api.com/en/API/FullCast/k_28nyce3o/' + entity_id).json()
    entity = Entity.objects.get(api_is=entity_id)

    # loop through json object and create variables for needed fields
    for item in data['actors']:
        api_id = item['id']
        image = item['image']
        name = item['name']
        asCharacter = item['asCharacter']

        try:
            actor = Actor.objects.get(api_id=api_id)
        except Actor.DoesNotExist:
            actor = Actor.objects.create(api_id=api_id, name=name, image=image)

        EntityActor.objects.create(entity=entity, actor=actor, asCharacter=asCharacter)

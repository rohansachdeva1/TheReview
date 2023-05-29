from django.contrib import admin
from .models import Medium, Genre, Entity, Category, Tag, EntityTag, Emotion

# Register your models here.
admin.site.register(Medium)
admin.site.register(Genre)
admin.site.register(Entity)
admin.site.register(Category)

admin.site.register(Tag)
admin.site.register(Emotion)
admin.site.register(EntityTag)
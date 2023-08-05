from django.contrib import admin
from .models import Medium, Genre, Entity, Category, Tag, EntityTag, Actor, EntityActor, StreamingService, EntityLocation
from .models import BaseEmotion, DerivedEmotion

# Register your models here.
admin.site.register(Medium)
admin.site.register(Genre)
admin.site.register(Entity)
admin.site.register(Category)

admin.site.register(Tag)
admin.site.register(BaseEmotion)
admin.site.register(DerivedEmotion)
admin.site.register(EntityTag)
admin.site.register(Actor)
admin.site.register(EntityActor)
admin.site.register(StreamingService)
admin.site.register(EntityLocation)

class DerivedEmotionsInline(admin.StackedInline):
    model = DerivedEmotion

class TagsInline(admin.StackedInline):
    model = Tag

class EmotionAdmin(admin.ModelAdmin):
    model = BaseEmotion
    fields = ["name"]
    inlines = [DerivedEmotionsInline, TagsInline]

admin.site.unregister(BaseEmotion)
admin.site.register(BaseEmotion, EmotionAdmin)


class EntityTagsInline(admin.StackedInline):
    model = EntityTag

class EntityActorsInline(admin.StackedInline):
    model = EntityActor

class EntityAdmin(admin.ModelAdmin):
    model = Entity
    fields = ["api_id", 
              "image", 
              "title", 
              "year", 
              "plot", 
              "medium", 
              "content_rating", 
              "runtime", 
              "overall_score",
              "genres",]
    inlines = [EntityTagsInline, EntityActorsInline]

admin.site.unregister(Entity)
admin.site.register(Entity, EntityAdmin)
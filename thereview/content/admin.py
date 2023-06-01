from django.contrib import admin
from .models import Medium, Genre, Entity, Category, Tag, EntityTag
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
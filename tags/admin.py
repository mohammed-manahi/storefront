from django.contrib import admin
from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Create tag model admin """
    search_fields = ["label"]

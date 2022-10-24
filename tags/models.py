from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    # Define custom manager for generic relation that uses content type for the tag(s) of a product with id
    def get_tags_for(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)
        return TaggedItem.objects.select_related("tag").filter(content_type=content_type, object_id=object_id)


class Tag(models.Model):
    """ Create Tag model """
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    """ Create TagItem model which applies generic tag using content_type """
    # Use the custom manager "TaggedItemManager"
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

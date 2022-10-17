from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    """ Create Tag model """
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    """ Create TagItem model which applies generic tag using content_type """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

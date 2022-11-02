from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    """ Serializer converts a model instance to a python dictionary to deal with json data"""
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)

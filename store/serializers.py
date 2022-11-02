""" Serializer converts a model instance to a python dictionary to deal with json data"""
from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)

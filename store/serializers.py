from store.models import Product, Collection
from rest_framework import serializers
from decimal import Decimal


# class CollectionSerializer(serializers.Serializer):
#     """ Create collection serializer """
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


# class ProductSerializer(serializers.Serializer):
#     """ Serializer converts a model instance to a python dictionary to deal with json data"""
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     # Add custom fields to serializer that are not defined in the model
#     product_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')
#     # Serializing relationships using string related object where django look for str method representation
#     # collection = serializers.StringRelatedField()
#     # Serializing relationships using primary key query set
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all())
#     # Serializing relationships using the collection serializer
#     # collection = CollectionSerializer()
#     # Serializing relationships using hyperlink to another end-point
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(), view_name="collection-detail")

#     def calculate_tax(self, product):
#         return product.unit_price * Decimal(1.1)

class CollectionSerializer(serializers.ModelSerializer):
    """ Instead of redefining serializer's fields, model serializer can be used for fields already defined in the model """
    class Meta():
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    """ Instead of redefining serializer's fields, model serializer can be used for fields already defined in the model """
    class Meta():
        model = Product
        fields = ["id", "title", "unit_price",
                  "collection", "product_with_tax"]

    # Add custom fields to serializer that are not defined in the model
    product_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)

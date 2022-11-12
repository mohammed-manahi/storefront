from store.models import Product, Collection, Review, Cart, CartItem
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
    """ Instead of redefining serializer's fields, model serializer can be used for fields already defined in  model """

    class Meta():
        model = Collection
        fields = ["id", "title", "product_count"]

    # Add custom field to get product count that belong a certain collection
    product_count = serializers.SerializerMethodField(method_name='get_product_count')

    def get_product_count(self, collection):
        return collection.products.count()


class ProductSerializer(serializers.ModelSerializer):
    """ Instead of redefining serializer's fields, model serializer can be used for fields already defined in  model """

    class Meta():
        model = Product
        fields = ["id", "title", "description", "slug", "unit_price",
                  "collection", "inventory", "product_with_tax"]

    # Add custom fields to serializer that are not defined in the model
    product_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    """ Create review serializer from review model """

    class Meta():
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        # Override create implementation to allow nested reviews in products
        product_id = self.context["product_id"]
        # Get product id defined in the views and unpack other validated data
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleRepresentationProductSerializer(serializers.ModelSerializer):
    """
    Create another product serializer from product model.
    This serializer contains only three fields for simple representation to be used for cart item serializer
    """

    class Meta():
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    """ Create cart item serializer from cart item model """

    # Redefine product object to get all product details from simple representation product serializer
    product = SimpleRepresentationProductSerializer()

    class Meta():
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    # Add custom fields to serializer that are not defined in the model
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    """ Create cart serializer from cart model """

    # Set id to read-only in order to only read it from backend to avoid post action from the client
    id = serializers.UUIDField(read_only=True)
    # Cart serializer relationship with cart item serializer and set items to read-only
    items = CartItemSerializer(many=True, read_only=True)

    class Meta():
        model = Cart
        fields = ["id", "items", "total_price"]

    # Add custom fields to serializer that are not defined in the model
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart):
        # Get the sum of all items in the cart
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

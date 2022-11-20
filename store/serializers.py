from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem
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


class AddCartItemSerializer(serializers.ModelSerializer):
    """
    Custom serializer to add cart item because logically only product id and quantity need to be added when adding a
    product to a cart. This implementation override base implementation where product title and unit price need to be
    filled to add product to cart item
    """
    product_id = serializers.IntegerField()

    class Meta():
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def validate_product_id(self, value):
        # Custom validation for product to prevent invalid product id by client
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with given id not found")
        return value

    def save(self, **kwargs):
        # Override default save method since add a product multiple times should increase the quantity not repeating id
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        # Read cart id using get serializer context defined in the views
        cart_id = self.context["cart_id"]

        # Define cart item using cart id and product id, if it doesn't exist create a new one
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # Update existing cart item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # Create a new cart item by unpacking validated data (product id and quantity)
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """
    Custom serializer to update cart item because logically only the quantity need to be updated when
    updating a product in a cart. This implementation override base implementation where product title and unit price
    need to be filled to update product to cart item
    """

    class Meta():
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    """ Create customer serializer from customer model """

    # Define user id for create action and make user id read only so client can't change it
    user_id = serializers.IntegerField(read_only=True)

    class Meta():
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]


class OrderItemSerializer(serializers.ModelSerializer):
    """ Create order item serializer from order item model """

    product = SimpleRepresentationProductSerializer()

    class Meta():
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """ Create order serializer from order model """

    customer = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True)

    class Meta():
        model = Order
        fields = ["id", "customer", "payment_status", "placed_at", "items"]

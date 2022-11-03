from django.db import models
from django.core.validators import MinValueValidator


class Collection(models.Model):
    """ Create Collection model """
    title = models.CharField(max_length=255)
    # Solve circular dependency using plus sign to avoid creating the reverse relationship
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    # String representation for the collection model
    def __str__(self):
        return self.title

    # Meta inner class for customizing items in django admin ui
    class Meta():
        ordering = ["title"]


class Promotion(models.Model):
    """ Create Promotion model and associate many-to-many relation with product model """
    description = models.CharField(max_length=256)
    discount = models.FloatField()


class Product(models.Model):
    """ Create Product model and associate many-to-one relation with collection model """
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    # Use django min value validator to ensure the price is larger than or equal to 1
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # Set on-delete to protect in order to prevent deleting all the products in the collection
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name="products")
    # Use plural "promotions" to indicate many-to-many- relation with promotion model
    promotions = models.ManyToManyField(
        Promotion, related_name="products", blank=True)

    # String representation for the product model
    def __str__(self):
        return self.title

    # Meta inner class for customizing items in django admin ui
    class Meta():
        ordering = ["title"]


class Customer(models.Model):
    """ Create Customer model """
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SLIVER = "S"
    MEMBERSHIP_GOLD = "G"
    # Set choices for membership and use bronze membership as default
    MEMBERSHIP_CHOICES = [(MEMBERSHIP_BRONZE, "Bronze"),
                          (MEMBERSHIP_SLIVER, "Sliver"), (MEMBERSHIP_GOLD, "Gold")]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    # String representation for the customer model
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Meta inner class for customizing items in django admin ui
    class Meta():
        ordering = ["first_name", "last_name"]


class Order(models.Model):
    """ Create Order model and associate many-to-one relation with customer model """
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    # Set choices for payment status and use pending status as default
    PAYMENT_STATUS_CHOICES = [(PAYMENT_STATUS_PENDING, "Pending"), (PAYMENT_STATUS_COMPLETE, "Complete"),
                              (PAYMENT_STATUS_FAILED, "Failed")]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # Set on-delete to protect in order to prevent deleting all the orders when customer is deleted
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    """ Create OrderItem model and associate many-to-one relation with order and product models """
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orderitems")
    quantity = models.PositiveSmallIntegerField()
    # Set unit_price to calculate the price at the time of order to allow varied prices
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    """ Create Cart model """
    # Auto_now_add populates only on creation
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """ Create CartItem model and associate many-to-one relation with cart and product models """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    """ Create Address model and associate many-to-one relation with customer model """
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # Set one-to-many relationship with customer where customer can have multiple addresses
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

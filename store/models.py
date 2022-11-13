from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
from django.conf import settings
from django.contrib import admin


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
    description = models.CharField(max_length=255)
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
    # The below fields are no longer needed since they are already defined in customized user model which is linked now
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    # Link customer with user model defined in settings after customization
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @admin.display(ordering="user__first_name")
    def first_name(self):
        # Define first name after linking customer to user and use it in admin
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        # Define last name after linking customer to user and use it in admin
        return self.user.last_name

    # String representation for the customer model
    def __str__(self):
        # Change first name and last name representations to user after linking customer to customized user model
        return f"{self.user.first_name} {self.user.last_name}"

    # Meta inner class for customizing items in django admin ui
    class Meta():
        # Change first name and last name ordering to user after linking customer to customized user model
        ordering = ["user__first_name", "user__last_name"]


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
    # Change base id integer with globally unique identifier to protect accessing to the cart
    id = models.UUIDField(primary_key=True, default=uuid4)
    # Auto_now_add populates only on creation
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """ Create CartItem model and associate many-to-one relation with cart and product models """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta():
        # Ensure single instance of product and just increase quantity
        unique_together = [["cart", "product"]]


class Address(models.Model):
    """ Create Address model and associate many-to-one relation with customer model """
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # Set one-to-many relationship with customer where customer can have multiple addresses
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Review(models.Model):
    """ Create Review model and associate many-to-one relation with product model """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from store import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """ Product model registration for django admin """
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    # Eager loading for related objects "collection" to the product model
    list_select_related = ["collection"]
    list_per_page = 20

    # Define computed component for inventory status and apply custom display ordering decorator
    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory <= 10:
            return "Low"
        else:
            return "OK"

    # Get the title from the related object collection model
    def collection_title(self, product):
        return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """ Customer model registration for django admin """
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 20

    # Display orders count's links and apply custom display ordering decorator
    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = reverse("admin:store_order_changelist") + "?" + urlencode({"customer__id": str(customer.id)})
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)

    # Override the base queryset to annotate orders count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """ Order model registration for django admin """
    list_select_related = ["customer"]
    list_display = ["customer_name", "placed_at"]
    ordering = ["-placed_at"]

    # Get the customer name from the related object customer model
    def customer_name(self, order):
        return f"{order.customer.first_name}, {order.customer.last_name}"


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    """ Product model registration for django admin """
    list_display = ["title", "products_count", "featured_product"]
    ordering = ["title"]

    # Display products count's links and apply custom display ordering decorator
    @admin.display(ordering="products_count")
    def products_count(self, collection):
        # override string return with links
        url = reverse("admin:store_product_changelist") + "?" + urlencode({"collection__id": str(collection.id)})
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)

    # Override the base queryset to annotate products count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))

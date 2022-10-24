from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Avg, Max, Min, Count
from store.models import Product, OrderItem, Collection, Promotion, Customer
from tags.models import TaggedItem


def query_sets(request):
    # A query set to get five sorted products of all products
    products = Product.objects.all().order_by("title", "collection__title")[:5]
    # A query set to get the product count
    product_count = Product.objects.count()
    # A query set to get the products that have been updated in year 2021 and select first 5 products
    recent_products = Product.objects.filter(last_update__year=2021)[:5]
    # A query set to get products that their prices are greater than 20 and their category is beauty
    filtered_products = Product.objects.filter(unit_price__gt=20).filter(collection__title="Beauty")[:5]
    # A query set to get products with a price range
    price_range_set = Product.objects.filter(unit_price__range=(50, 60))[:5]
    # A query set that uses Q object to get products which are either less than 10 in the inventory or their prices are greater than 20
    products_q_objects = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=20))[:5]
    # A query set that uses F object to get products' inventory which are equal to products' prices
    products_f_objects = Product.objects.filter(inventory=F("unit_price"))
    # A query set to sort products by highest price and descending order title
    highest_products = Product.objects.order_by("-unit_price", "-title")[:5]
    # A query set to get certain values form the model fields
    products_certain_fields = Product.objects.values("title", "collection")[:5]
    # A query set to get the product titles that have been ordered
    ordered_products = Product.objects.filter(id__in=OrderItem.objects.values("product__id")).distinct().order_by(
        "title")[:5]
    # A query set to get product categories using select related which is used when the model has one instance
    product_categories = Product.objects.select_related("collection").all()[:5]
    # A query set to get product promotions using prefetch related which is used when the model has many instances
    product_promotions = Product.objects.prefetch_related("promotions").select_related("collection").all()[:5]
    # A query set to get last five orders with their customers and product titles
    last_orders = OrderItem.objects.select_related("product").select_related("order").filter(
        order__payment_status="C").order_by("-order__placed_at")[:5]
    # A query set to get min price in beauty category using aggregate
    min_price_in_beauty_collection = Product.objects.filter(collection__title="Beauty").aggregate(
        min_price=Min("unit_price"))
    # A query set to annotate customer full name using concatenation
    customer_full_names = Customer.objects.annotate(full_name=Func(F("first_name"), Value(' '), F("last_name"),
                                                                   function="CONCAT"))[:5]
    # A query set to count the number of orders for each customer
    customer_orders = Customer.objects.annotate(orders_count=Count('order'))[:5]
    # ِA query set to apply discount using expression wrapper
    discount = ExpressionWrapper(F("unit_price") * 0.8, output_field=DecimalField())
    discounted_price = Product.objects.annotate(discount=discount)
    # A query set for generic relation that uses content type for the tag(s) of a product with id 1
    content_type = ContentType.objects.get_for_model(Product)
    product_tags = TaggedItem.objects.select_related("tag").filter(content_type=content_type, object_id=1)
    # A query set to achieve the generic relation above using custom manager defined in tags app's models
    TaggedItem.objects.get_tags_for(Product, 1)

    template = "query_set.html"
    context = {"products": products, "recent_products": recent_products, "filtered_products": filtered_products,
               "price_range_set": price_range_set, "products_q_objects": products_q_objects,
               "product_count": product_count, "products_f_objects": products_f_objects,
               "highest_products": highest_products, "products_certain_fields": products_certain_fields,
               "ordered_products": ordered_products, "product_categories": product_categories,
               "product_promotions": product_promotions, "last_orders": last_orders,
               "min_price_in_beauty_collection": min_price_in_beauty_collection,
               "customer_full_names": customer_full_names, "customer_orders": customer_orders,
               "product_tags": product_tags}
    return render(request, template, context)

from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product


def query_sets(request):
    # A query set to get all products
    products = Product.objects.all()
    # A query set to get the products that have been updated in year 2021 and select first 5 products
    recent_products = Product.objects.filter(last_update__year=2021)[:5]
    # A query set to get products that their prices are greater than 20 and their category is beauty
    filtered_products = Product.objects.filter(unit_price__gt=20).filter(collection__title="Beauty")[:5]
    # A query set to get products with a price range
    price_range_set = Product.objects.filter(unit_price__range=(50, 60))[:5]
    # A query set that uses Q object to get products which are either less than 10 in the inventory or their prices are greater than 20
    products_q_objects = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=20))[:5]
    # A query set that uses Q object to get products' inventory which are equal to products' prices
    products_f_objects = Product.objects.filter(inventory=F("unit_price"))
    template = "query_set.html"
    context = {"products": products, "recent_products": recent_products, "filtered_products": filtered_products,
               "price_range_set": price_range_set, "products_q_objects": products_q_objects}
    return render(request, template, context)

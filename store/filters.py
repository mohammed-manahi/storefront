""" Custom filter based on django-filter library for unit price to allow less than and greater than """
from store.models import Product
from django_filters.rest_framework import FilterSet


class ProductFilter(FilterSet):
    """ Custom filter class to modify unit price default filter"""

    class Meta():
        model = Product
        # Keep default filter for collection id and apply custom filter for unit price
        fields = {
            "collection_id": ["exact"],
            "unit_price": ["gt", "lt"],
        }

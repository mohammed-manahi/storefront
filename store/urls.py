from django.urls import path, include
from store import views

urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),

    # path("products/", views.product_list, name="products"),
    # Use url routes for class-based products view instead of function-based
    path("products/", views.ProductList.as_view(), name="products"),

    # path("products/<int:pk>", views.product_detail, name="product-detail"),
    # Use url routes for class-based product detail view instead of function-based
    path("products/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),

    # path("collections/", views.collection_list, name="collections"),
    # path("collections/<int:pk>", views.collection_detail, name="collection-detail")
]

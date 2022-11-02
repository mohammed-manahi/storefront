from django.urls import path, include
from store import views

urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),
    path("products/", views.product_list, name="products"),
    path("products/<int:pk>", views.product_detail, name="product-detail"),
    path("collections/<int:pk>", views.collection_detail, name="collection-detail")
]

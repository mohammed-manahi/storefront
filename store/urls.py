from django.urls import path, include
from store import views

urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),
    path("products/", views.product_list, name="products"),
    path("products/<int:id>", views.product_detail, name="product_detail")
]

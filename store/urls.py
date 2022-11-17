from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from store import views
from rest_framework_nested import routers

# Use DRF nested router to register view set routes
router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet, basename="carts")
router.register("customers", views.CustomerViewSet, basename="customers")
# urlpatterns = router.urls


# Set nested router using library drf-nested-routers for reviews in product
product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
# Register child resources (nested routes)
product_router.register('reviews', views.ReviewViewSet, basename="product-reviews")
# Set nested router using library drf-nested-routers for cart items in cart
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
# Register child resources (nested routes)
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),
    # Include view set routers
    path(r"", include(router.urls)),
    # Include nested routers
    path(r"", include(product_router.urls)),
    path(r"", include(cart_router.urls)),
]

# urlpatterns = [
#     # path("products/", views.product_list, name="products"),
#     # Use url routes for class-based products view instead of function-based
#     path("products/", views.ProductList.as_view(), name="products"),
#
#     # path("products/<int:pk>", views.product_detail, name="product-detail"),
#     # Use url routes for class-based product detail view instead of function-based
#     path("products/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
#
#     # path("collections/", views.collection_list, name="collections"),
#     # Use url routes for class-based products view instead of function-based
#     path("collections/", views.CollectionList.as_view(), name="collections"),
#
#     # path("collections/<int:pk>", views.collection_detail, name="collection-detail")
#     # Use url routes for class-based products view instead of function-based
#     path("collections/<int:pk>", views.CollectionDetail.as_view(), name="collection-detail")
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store import views

# Use DRF router to register view set routes
router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")
urlpatterns = router.urls

# urlpatterns = [
#     path("__debug__/", include('debug_toolbar.urls')),
#
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

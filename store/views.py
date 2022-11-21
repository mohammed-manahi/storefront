from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import ProductFilter
from store.models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order
from store.permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from store.serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, \
    CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, \
    CreateOrderSerializer, UpdateOrderSerializer


# @api_view(["GET", "POST"])
# def product_list(request):
#     # DRF serialization for getting products data
#     if request.method == "GET":
#         products = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(
#             products, many=True, context={"request": request})
#         return Response(serializer.data)
#     # DRF deserialization for posting products data
#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def product_detail(request, pk):
#     # Render product detail using the serializer data to json
#     # try:
#     #     product_detail = Product.objects.get(pk=id)
#     #     product_serializer = ProductSerializer(product_detail)
#     #     return Response(product_serializer.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)
#     product = get_object_or_404(Product, pk=pk)
#     # DRF serialization for getting a product data
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     # DRF deserialization for updating a product data
#     elif request.method == "PUT":
#         serializer = ProductSerializer(instance=product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # DRF deserialization for deleting a product data
#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response({"error": "Product is associated with an order item"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         else:
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(["GET", "POST"])
# def collection_list(request):
#     # DRF serialization for getting collections data
#     if request.method == "GET":
#         collection = Collection.objects.all()
#         serializer = CollectionSerializer(
#             collection, many=True, context={"request": request})
#         return Response(serializer.data)
#     # DRF serialization for posting collections data
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     # DRF serialization for getting a collection data
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     # DRF deserialization for updating a collection data
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(
#             instance=collection, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # DRF deserialization for deleting a collection data
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:
#             return Response({"error": "Collection has associated product(s)"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         else:
#             collection.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(APIView):
#     """ Class-based view for product list API using DRF APIView class"""
#
#     def get(self, request):
#         # DRF serialization for getting products data
#         products = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(products, many=True, context={"request": request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         # DRF deserialization for posting products data
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class ProductDetail(APIView):
#     """ Class-based view for product detail API using DRF APIView class """
#
#     def get(self, request, pk):
#         # DRF serialization for getting a product data
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         # DRF deserialization for updating a product data
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(instance=product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         # DRF deserialization for deleting a collection data
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({"error": "Product is associated with an order item"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         else:
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
# class ProductList(ListCreateAPIView):
#     """ Generic class-based view for product list API using DRF generic ListCreateAPIView
#         class. This implementation includes list (get) and create (post) for products
#     """
#
#     def get_queryset(self):
#         # Define products API query-set
#         return Product.objects.select_related("collection").all()
#
#     def get_serializer_class(self):
#         # Define product API serializer
#         return ProductSerializer
#
#     def get_serializer_context(self):
#         # Define product API context
#         return {"request": self.request}
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     """ Generic class-based view for product detail API using DRF generic RetrieveUpdateDestroyAPIView
#         class. This implementation includes retrieve (get) update (update) and delete (destroy)
#         for a product instance
#     """
#
#     def get_queryset(self):
#         # Define API product query-set
#         return Product.objects.all()
#
#     def get_serializer_class(self):
#         # Define product API serializer
#         return ProductSerializer
#
#     def delete(self, request, pk):
#         # Override base implementation's delete method to apply custom delete logic
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({"error": "Product is associated with an order item"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         else:
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class CollectionList(ListCreateAPIView):
#     """ Generic class-based view for collection list API using DRF generic ListCreateAPIView
#         class. This implementation includes list (get) and create (post) for collections
#     """
#
#     def get_queryset(self):
#         # Define collections API query-set
#         return Collection.objects.all()
#
#     def get_serializer_class(self):
#         # Define collection API serializer
#         return CollectionSerializer
#
#     def get_serializer_context(self):
#         # Define collection API context
#         return {"request": self.request}
#
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     """ Generic class-based view for collection detail API using DRF generic RetrieveUpdateDestroyAPIView
#         class. This implementation includes retrieve (get) update (update) and delete (destroy)
#         for a collection instance
#     """
#
#     def get_queryset(self):
#         # Define API collection query-set
#         return Collection.objects.all()
#
#     def get_serializer_class(self):
#         # Define collection API serializer
#         return CollectionSerializer
#
#     def delete(self, request, pk):
#         # Override base implementation's delete method to apply custom delete logic
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({"error": "Collection has associated product(s)"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         else:
#             collection.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    """ Model view set for product provides more generic implementation which includes get, post, update,
        and delete together """

    # Use django-filter library to apply generic back-end filtering and search filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["collection_id", "unit_price"]
    # Use custom filter called filters defined in the store app to apply lt and gt for unit price
    filterset_class = ProductFilter
    # Add search filter fields
    search_fields = ["title", "description"]
    # Add sorting filter fields
    ordering_fields = ["unit_price", "last_update"]

    # Set permission for product endpoint using custom permission defined in permissions.py
    permission_classes = [IsAdminOrReadOnly]

    # Blow code snippet is no longer needed since pagination is applied globally to all endpoints
    # Add pagination for product list
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        # Define product API query-set and filter products based on their collections
        return Product.objects.all()

        # Blow code snippet is no longer needed since django-filter library is applied
        # products = Product.objects.all()
        # collection_id = self.request.query_params.get("collection_id")
        # if collection_id is not None:
        #     # Update the query set if collection exists
        #     products = products.filter(collection_id=collection_id)
        # return products

    def get_serializer_class(self):
        # Define product API serializer
        return ProductSerializer

    def get_serializer_context(self):
        # Define product API context
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        # Override base implementation's delete method to apply custom delete logic
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error": "Product is associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    """ Model view set for collection provides more generic implementation which includes get, post, update,
        and delete together """

    # Set permission for collection endpoint
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        # Define collection API query-set
        return Collection.objects.all()

    def get_serializer_class(self):
        # Define collection API serializer
        return CollectionSerializer

    def get_serializer_context(self):
        # Define collection API context
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        # Override base implementation's delete method to apply custom delete logic
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({"error": "Collection has associated product(s)"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    """ Model view set for Review """

    def get_queryset(self):
        # Define review API query-set
        # Apply query-set to show reviews on reviewed products only
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_class(self):
        # Define review API serializer
        return ReviewSerializer

    def get_serializer_context(self):
        # Define review API context, use product pk to autopopulate product id in review post http method
        return {"request": self.request, "product_id": self.kwargs["product_pk"]}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Custom view set using create model mixin for cart because cart doesn't have list or update.
    Cart should not implement list or update actions.
    List and update features are available for cart items and should not be implemented for cart itself.
    """

    def get_queryset(self):
        # Define cart API query-set and use eager load for items to fine-tune sql queries
        return Cart.objects.select_related("customer").prefetch_related("orderitems").all()

    def get_serializer_class(self):
        # Define cart API serializer
        return CartSerializer


class CartItemViewSet(ModelViewSet):
    """ Model view set for cart item """

    # Prevent put http method from allowed http method because only quantity field is updated using patch http method
    # Note: method names should be in lower case
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        # Define cart item API query-set and filter by cart id because the endpoint is nested in routes
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"]).select_related("product").all()

    def get_serializer_class(self):
        # Define cart item API serializer and apply custom cart item serializer if the request is post
        if self.request.method == "POST":
            # Reason for this is explained in add cart item serializer in serializers
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            # Only patch http method is checked because only quantity field is updated
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        # Define cart item API context and set cart id because the endpoint is nested in routes
        return {"request": self.request, "cart_id": self.kwargs["cart_pk"]}


class CustomerViewSet(ModelViewSet):
    """
    Model view set for customer where list and delete actions should not be implemented here.
    List and delete actions should be only in admin panel.
    """

    # Set permission for customer's endpoint, note that IsAdminUser is provided by django rest framework
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     # Set permission based on http method. Note here we pass object of the permission
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def get_queryset(self):
        # Define customer API query-set
        return Customer.objects.all()

    def get_serializer_class(self):
        # Define customer API serializer
        return CustomerSerializer

    def get_serializer_context(self):
        # Define customer API context
        return {"request": self.request}

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        # Define a new action for getting current user's profile and set detail to false to show list not detail
        # Handle user is not a customer by using get or create which returns a tuple of object and boolean if created
        # The below code is no longer needed since a signal for customer creation creates a new user
        # (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(instance=customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        # Define a new action based on custom model permission defined in customer model
        return Response("OK")


class OrderViewSet(ModelViewSet):
    " Model view set for order """

    # Set permission classes for order viewset
    # permission_classes = [IsAuthenticated]

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        # Custom permission method to prevent client from performing put and delete http methods
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Override create to return order items instead of cart id
        serializer = CreateOrderSerializer(data=request.data, context={"user_id": self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # order object is fetched from serializer to return order items
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        # Define order API query-set, where staff can view all orders and client can view only his/her own order
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items").all()
        # The below code is no longer needed since a signal for customer creation creates a new user
        # (customer_id, created) = Customer.objects.only("id").get_or_create(user_id=self.request.user.id)
        customer_id = Customer.objects.only("id").get(user_id=self.request.user.id)
        return Order.objects.filter(customer_id=customer_id)

    def get_serializer_class(self):
        # Define order API serializer
        if self.request.method == "POST":
            return CreateOrderSerializer
        if self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        # Define order API context
        return {"request": self.request, "user_id": self.request.user.id}

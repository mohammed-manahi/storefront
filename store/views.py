from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from store.models import Product, Collection, OrderItem
from store.serializers import ProductSerializer, CollectionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet


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

    def get_queryset(self):
        # Define products API query-set
        return Product.objects.all()

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

    def get_queryset(self):
        # Define collections API query-set
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

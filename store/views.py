from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from store.models import Product
from store.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST"])
def product_list(request):
    # DRF serialization for getting data
    if request.method == "GET":
        products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            products, many=True, context={"request": request})
        return Response(serializer.data)
    # DRF deserialization for posting data
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    # Render product detail using the serializer data to json
    # try:
    #     product_detail = Product.objects.get(pk=id)
    #     product_serializer = ProductSerializer(product_detail)
    #     return Response(product_serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    product = get_object_or_404(Product, pk=pk)
    # DRF serialization for getting data
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    # DRF deserialization for updating data
    elif request.method == "PUT":
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DRF deserialization for deleting data
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({"error": "Product is associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request, pk):
    return Response("OK")

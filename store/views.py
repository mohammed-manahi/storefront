from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from store.models import Product
from store.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST"])
def product_list(request):
    # Django rest framework serialization
    if request.method == "GET":
        products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            products, many=True, context={"request": request})
        return Response(serializer.data)
    # Django rest framework deserialization
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            return Response("OK")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def product_detail(request, pk):
    # Render product detail using the serializer data to json
    # try:
    #     product_detail = Product.objects.get(pk=id)
    #     product_serializer = ProductSerializer(product_detail)
    #     return Response(product_serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    product_detail = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product_detail)
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    return Response("OK")

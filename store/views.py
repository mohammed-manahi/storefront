from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def product_list(request):
    # Django rest framework uses api view decorator and response class
    return Response("OK")


@api_view()
def product_detail(request, id):
    return Response(id)

from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    just_for_debugging = 10
    context = {"name": "Mohammed"}
    return render(request, "hello.html", context)

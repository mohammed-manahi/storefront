from django.urls import path
from playground import views

urlpatterns = [
    path("hello/", views.say_hello, name="hello"),
]

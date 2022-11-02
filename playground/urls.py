from django.urls import path, include
from playground import views

urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),
    path("query-sets/", views.query_sets, name="query_sets"),
]

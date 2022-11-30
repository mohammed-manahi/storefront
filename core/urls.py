from django.views.generic import TemplateView
from django.urls import path, include
from core import views

urlpatterns = [
    # Add home page url using generic template view
    path("", TemplateView.as_view(template_name="core/index.html")),
]

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """ Register User admin again after customizing the user admin and get fieldsets from base user admin """
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                # Add email, first name and last name fields to default fields
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


""" Ensure decoupling and self-contained by moving the tag inline admin model to a custom app """


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from store.models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    # Use signals to create customer for each new user instance
    if kwargs["created"]:
        # created is boolean value that indicates that a customer is created
        Customer.objects.create(user=kwargs["instance"])

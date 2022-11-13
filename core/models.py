from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extend user class by inheriting abstract user class to make email field unique.
    This process should always be applied at the begggining of the project, otherwise all database should be dropped
    and created again.
    """
    email = models.EmailField(unique=True)

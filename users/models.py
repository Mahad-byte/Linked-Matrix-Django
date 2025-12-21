from django.db import models
from .enums import user_group
from .custommanager import CustomManagerProxy, CustomUserManager
from django.core.validators import validate_email

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Create your models here.
def check_email(value):
        if value.endswith("@gmail.com"):
            raise ValueError("Not a valid email")


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        validators=[validate_email, check_email],
    )
    groups = models.CharField(
        max_length=1,
        choices=user_group,
        default='B'
    )
    phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    # Field Properties
    @property
    def display_name(self):
        return f"{self.first_name}-$"
    
    def __str__(self):
        return f"{self.email}"
    
    # Meta (Inner Class)
    class Meta:
         verbose_name = 'User'
         ordering = ['-created_at']


# Users who have not made a post yet
class ProxyUsers(get_user_model()):

    objects = CustomManagerProxy()
        
    class Meta:
        proxy = True 
        verbose_name = 'Proxy Users'
    

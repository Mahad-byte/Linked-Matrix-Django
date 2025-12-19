from django.db import models
from .enums import user_group
from .custommanager import CustomManagerProxy, CustomUserManager
from django.core.validators import validate_email

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

class Tags(models.Model):
     name = models.CharField(max_length=50)
     slug = models.SlugField(max_length=50)
     class Meta:
          verbose_name = 'Tag'


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey( # One-to-Many
        User,
        on_delete=models.CASCADE,           
        null=True,                          
        blank=True,                         
        verbose_name='post author',        
        db_column='author_id',             
        db_constraint=True,                 
        db_index=True,                      
    )
    tag = models.ManyToManyField(Tags, related_name='posts') # Many-to-Many
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
         verbose_name = 'Post'
         

# Single Like Model for multiple Models like Post, Comment, etc.
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
    

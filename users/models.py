from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser


# Create your models here.
def check_email(value):
        if value.endswith("@gmail.com"):
            raise ValueError("Not a valid email")


class User(models.Model):
    email = models.EmailField(max_length=50, validators=[check_email, validate_email])
    password = models.CharField(max_length=20, )
    is_business = models.BooleanField(default=0)


class SimpleUser(AbstractUser):
    phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    # Field Properties
    @property
    def display_name(self):
        return f"{self.first_name}-$"
    
    def __str__(self):
        return f"{self.username}"
    
    # Meta (Inner Class)
    class Meta:
         verbose_name = 'Simple User'
         ordering = ['-created_at']



class Tags(models.Model):
     name = models.CharField(max_length=50)
     slug = models.SlugField(max_length=50)
     class Meta:
          verbose_name = 'Tag'


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey( # One-to-Many
        SimpleUser,
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
         



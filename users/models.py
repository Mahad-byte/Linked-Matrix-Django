from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser


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
    phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
         



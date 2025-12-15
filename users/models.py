from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

def check_email(value):
        if value.endswith("@gmail.com"):
            raise ValueError("Not a valid email")

class User(models.Model):
    # firstname = models.CharField(max_length=255)
    # lastname = models.CharField(max_length=255)
    # email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20, validators=[check_email, validate_email])
    is_business = models.BooleanField(default=0)

class SimpleUser(AbstractUser):
     
     phone_number = models.CharField(max_length=11)


    
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        SimpleUser,
        on_delete=models.CASCADE,           
        null=True,                          
        blank=True,                         
        verbose_name='post author',        
        db_column='author_id',             
        db_constraint=True,                 
        db_index=True,                      
    )
    created_at = models.DateTimeField(auto_now_add=True)    


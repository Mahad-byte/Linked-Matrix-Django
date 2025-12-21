from django.db import models
from users.models import User
from tags.models import Tags

# Create your models here.
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
         

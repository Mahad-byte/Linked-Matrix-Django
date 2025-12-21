from django.db import models

# Create your models here.
class Tags(models.Model):
     name = models.CharField(max_length=50)
     slug = models.SlugField(max_length=50)
     class Meta:
          verbose_name = 'Tag'

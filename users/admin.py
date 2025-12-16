from django.contrib import admin
from .models import SimpleUser


class ModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(SimpleUser)

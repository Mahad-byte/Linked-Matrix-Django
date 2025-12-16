from django.contrib import admin
from .models import SimpleUser, Post, Tags


class ModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(SimpleUser)
admin.site.register(Post)
admin.site.register(Tags)

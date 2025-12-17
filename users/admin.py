from django.contrib import admin
from .models import SimpleUser, Post, Tags


@admin.action(description='Mark selected users as inactive')
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
    

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    list_filter = ('phone_number', 'username')
    search_fields = ('username__startswith', )
    fields = ('first_name', 'username', 'last_name', 'phone_number', 'email', 'is_staff', 'is_active')
    model_order = ['Simple User', 'Post', 'Tag']
    actions = [mark_inactive]


# Register your models here.
admin.site.register(SimpleUser, UserAdmin)
admin.site.register(Post)
admin.site.register(Tags)


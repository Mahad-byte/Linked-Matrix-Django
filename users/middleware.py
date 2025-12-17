from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden


class CustomMiddleware(MiddlewareMixin):
    
    def process_request(self, request): 
        if request.path == '/admin/':
            if request.user.email != 'admin@admin.com':
                return HttpResponseForbidden("You are not allowed to access the admin panel.")
            
        if request.path == '/login/':
            if request.user.is_authenticated:
                if request.user.email == 'admin@admin.com':
                    return HttpResponseForbidden("Admin user cannot access the login page.")
                
        elif request.path == '/home/':
            if request.user.email == 'admin@admin.com':
                    return HttpResponseForbidden("Admin user cannot access the home page.")
            
            
        
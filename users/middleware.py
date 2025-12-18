from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.core import cache
from logging import getLogger

class CustomMiddleware(MiddlewareMixin):
    
    def process_request(self, request): 
        logger = getLogger('request_logger')
        ip_address = request.META.get('REMOTE_ADDR')
        logger.info(f"IP Address: {ip_address}")
        count = cache.cache.get(ip_address, 0)
        count += 1
        cache.cache.set(ip_address, count, timeout=60)
        logger.info(f"User: {request.user.email}, Count: {count}")
        if count > 5:
            logger.error(f"User Blocked due to rate limit exceeded") 
            return JsonResponse(
                {'error': 'Too many requests. Please try again later.'}, 
                status=429
            )
        
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
            
            
    
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.core import cache
from logging import getLogger

from .enums import user_group
from .utils import increment_counter, check_counter

class CustomMiddleware(MiddlewareMixin):
    
    def check_block_key(self, logger, block_key):
        if cache.cache.get(block_key):
            logger.warning("User will be unblocked after 60 seconds") 
            return JsonResponse(
                {'error': 'Too many requests for Bronze group. Please try again later.'}, 
                status=429
            )
    
    def process_request(self, request): 
        logger = getLogger('request_logger')
        ip_address = request.META.get('REMOTE_ADDR')
        logger.info(f"IP Address: {ip_address}")
        
        # Block key, set once when limit exceeded
        # group = request.user.groups if request.user.is_authenticated else None
        # block_key = f"block_{ip_address}_{group}" if group is not None else f"block_{ip_address}_unauthenticated"
        
        # unauthenticated = f"{ip_address}_unauthenticated" 
        # key = f"{ip_address}_{group}" if request.user.is_authenticated else unauthenticated

        # LIMIT = user_group.get(group) if user_group.get(group) else 1
        # if (response:=self.check_block_key(logger, block_key)):
        #     return response

        # counter = increment_counter(cache.cache, key, ttl=60)
        # print(counter, LIMIT)
        
        # if (response:= check_counter(group, cache.cache, block_key, counter, LIMIT, logger)):
        #     return response

             
        # Admin & User Restrictions
        if request.user.is_authenticated:
            if request.path == '/admin/':
                if request.user.email != 'admin@admin.com':
                    return HttpResponseForbidden("You are not allowed to access the admin panel.")
                
            elif request.path == '/login/':
                if request.user.is_authenticated:
                    if request.user.email == 'admin@admin.com':
                        return HttpResponseForbidden("Admin user cannot access the login page.")
                    
            elif request.path == '/home/':
                if request.user.email == 'admin@admin.com':
                        return HttpResponseForbidden("Admin user cannot access the home page.")
                    
    
                
            
    
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.core import cache
from logging import getLogger

class CustomMiddleware(MiddlewareMixin):
    
    def process_request(self, request): 
        logger = getLogger('request_logger')
        ip_address = request.META.get('REMOTE_ADDR')
        logger.info(f"IP Address: {ip_address}")
        
        # Task 2
        # count = cache.cache.get(ip_address, 0)
        # count += 1
        # cache.cache.set(ip_address, count, timeout=60)
        # logger.info(f"User: {request.user.email}, Count: {count}")
        # if count > 5:
        #     logger.error(f"User Blocked due to rate limit exceeded") 
        #     return JsonResponse(
        #         {'error': 'Too many requests. Please try again later.'}, 
        #         status=429
        #     )
        
        user_groups = {
            'B': 2,  
            'S': 5,  
            'G': 10 
        }
        
        if request.user.is_authenticated:
            group = request.user.groups
            LIMIT = user_groups.get(group)
            
            # Block key, set once when limit exceeded
            block_key = f"block_{ip_address}_{group}"
            
            if cache.cache.get(block_key):
                return JsonResponse(
                    {'error': 'Too many requests for Bronze group. Please try again later.'}, 
                    status=429
                )
            
            # Counter Key
            key = f"{ip_address}_{group}"
            counter = cache.cache.get(key)
            print("Counter:", counter)

            if counter is None:  
                cache.cache.set(key, 1, timeout=60)
                counter = 1
            else:
                counter = cache.cache.incr(key)
            
            logger.info(f"User {request.user.email} Accessed {counter} times")

            if counter > LIMIT:
                logger.error(f"{ip_address}_{group}", counter)
                cache.cache.set(block_key, True, timeout=60)
                logger.error(f"User Blocked due to Bronze group rate limit exceeded") 
                logger.warning("User will be unblocked after 60 seconds") 

                return JsonResponse(
                    {'error': 'Too many requests for Bronze group. Please try again later.'}, 
                    status=429
                )
        else:
            logger.info("Anonymous User")
            
            # Block key, set once when limit exceeded
            block_unauth = f"block_{ip_address}_unauthenticated"
            
            if cache.cache.get(block_unauth):
                return JsonResponse(
                    {'error': 'Too many requests. Please try again later.'}, 
                    status=429
                )
            
            # Counter Key
            unauthenticated = f"{ip_address}_unauthenticated"
            count = cache.cache.get(unauthenticated)
            
            if count is None:
                cache.cache.set(unauthenticated, 1, timeout=60)
                count = 1
            else:
                count = cache.cache.incr(unauthenticated)
                
            print("Count:", count)
            
            if count > 1:
                cache.cache.set(block_unauth, True, timeout=60)
                logger.error(f"Anonymous User Blocked due to rate limit exceeded") 
                logger.warning("unauthenticated user will be unblocked after 60 seconds") 

                return JsonResponse(
                    {'error': 'Too many requests. Please try again later.'}, 
                    status=429
                )
               
            
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
                
            
    
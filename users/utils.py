from django.contrib.contenttypes.models import ContentType
from .models import Like, Post
from django.http import JsonResponse
from logging import getLogger



def attach_is_liked(posts, user):
    post_type = ContentType.objects.get_for_model(Post)
    for post in posts:
        post.is_liked = Like.objects.filter(
            user=user,
            content_type=post_type,
            object_id=post.id,
            is_liked=True
        ).exists()
    return posts


def increment_counter(cache, key, ttl=60):
    value = cache.get(key)
    if value is None:
        cache.set(key, 1, timeout=ttl)
        return 1
    
    return cache.incr(key)
    
    
def check_counter(group, cache, key, count, limit, logger):

    if count > limit:
        cache.set(key, True, timeout=60)
        logger.error(f"User Blocked due to {group} group rate limit exceeded") 
        return JsonResponse(
                {'error': f'Too many requests for {group} group. Please try again later.'}, 
                status=429
            )
    return False
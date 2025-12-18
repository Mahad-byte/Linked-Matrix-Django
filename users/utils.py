from django.contrib.contenttypes.models import ContentType
from .models import Like, Post


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
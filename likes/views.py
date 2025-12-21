import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.contrib.contenttypes.models import ContentType
from likes.models import Like

# Create your views here.
@login_required  
def like_post(request):
    data = json.loads(request.body)
    user = request.user
    print(user)
    post_id = data.get('post_id')
    print("post ID: ", post_id)
    
    post = Post.objects.get(id=post_id)
    content_type_post = ContentType.objects.get_for_model(Post)
    check_like, created = Like.objects.get_or_create(
        user=user,  
        content_type=content_type_post,
        object_id=post.id
    )
    print(check_like)
    if check_like:
        check_like.is_liked = not check_like.is_liked
        check_like.save()
        return_json = {
            'status': 'success',
            'message': check_like.is_liked
        }
        return JsonResponse(return_json)

from pyexpat.errors import messages
from django.views.generic import ListView
from posts.models import Post
from django.http import JsonResponse
from users.utils import attach_is_liked
import json


# Create your views here.
class PostView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created_at')
        return attach_is_liked(posts, self.request.user)
    
    

def update_post(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            post_id = data.get('post_id')
            new_text = data.get('new_text')
            
            try:
                post = Post.objects.get(id=post_id)
                post.title = new_text
                post.save()
            except Post.DoesNotExist:
                messages.error(request, "Post does not exist.")
        
        return JsonResponse({'status': 'success'})
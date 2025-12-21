from django.views.generic import ListView
from posts.models import Post
from users.utils import attach_is_liked


# Create your views here.
class PostView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created_at')
        return attach_is_liked(posts, self.request.user)
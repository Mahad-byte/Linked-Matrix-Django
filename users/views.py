import json
from django.http import JsonResponse

from .models import User, Post, Like
from django.views.generic import ListView
from .utils import attach_is_liked

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect


# Create your views here.
def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')
             
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = get_user_model()
        user = user.objects.get(email=email)
        print(user.password, password)
        check = check_password(password, user.password)
        if not check:
            messages.error(request, "Invalid password.")
            return render(request, 'login.html')

        if not user.is_active:
            messages.error(request, "This account is inactive")
            return render(
                    request, 
                    'login.html',
                    {'error': 'This account is inactive'},
                    status=403  
                )    
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            print("Authenticated: ", user)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def signin_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                    return render(request, 'sigin.html')
                
                # Create the user
                user = User.objects.create_user(email=email, username=username, password=password)
                print(f"User created: {user}")
                
                user_mddel = get_user_model()
                userr = user_mddel.objects.get(email=email)
                print(userr.password, password)
                check = check_password(password, userr.password)
                if not check:
                    messages.error(request, "Invalid password.")
                    return render(request, 'login.html')
                
                # Authenticate and login
                user = authenticate(request, email=email, password=password)
                print("Authenticate: ", user)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
                return render(request, 'sigin.html')

    return render(request, 'sigin.html')


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required
def home_page(request):

    print(f"Is authenticated: {request.user.is_authenticated}")

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    user_posts = attach_is_liked(user_posts, request.user)
    
    context ={
        'user': request.user,
        'posts': user_posts
    }
    return render(request, 'home.html', context)


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


class PostView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created_at')
        return attach_is_liked(posts, self.request.user)
            

    
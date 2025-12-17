from .models import User, Post
from django.views.generic import ListView

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect


# Create your views here.
def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')
             
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = get_user_model()
        user = user.objects.get(username='user1')
        print(user.is_active)
        # user.set_password(password)
        # user.save()
        
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
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            print("Authenticated: ", user)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def signin_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                    return render(request, 'login.html')
                
                # Create the user
                user = User.objects.create_user(username=username, password=password)
                print(f"User created: {user}")
                
                # Authenticate and login
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
                return render(request, 'login.html')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required
def home_page(request):

    print(f"Is authenticated: {request.user.is_authenticated}")

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    context ={
        'user': request.user,
        'posts': user_posts
    }
    return render(request, 'home.html', context)


class PostView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_posts(self):
        return Post.objects.all().order_by('-created_at')
    
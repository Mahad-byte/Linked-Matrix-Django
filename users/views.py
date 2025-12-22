from users.models import User
from posts.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from users.utils import attach_is_liked


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
        password = request.POST.get('password')
        
        if email and password:
            try:
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                    return render(request, 'sigin.html')
                
                # Create the user
                user = User.objects.create_user(email=email, password=password)
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
    user_posts = attach_is_liked(user_posts, request.user) # TODO: Do with annotate()
    
    context ={
        'user': request.user,
        'posts': user_posts
    }
    return render(request, 'home.html', context)

            

    
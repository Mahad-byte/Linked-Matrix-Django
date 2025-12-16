from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SimpleUser

# Create your views here.
def login_page(request):
    print("request: ", request)
    if request.user.is_authenticated:
        return redirect('home')
    
    from django.contrib.auth import get_user_model

    User = get_user_model()
    print("All users in database:", User.objects.all())
    user = SimpleUser.objects.get(username='user2')
    print(user.is_active)
    print("Usernames:", list(User.objects.values_list('username', flat=True)))
            
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth.hashers import check_password
        print(password, user.password)
        print(f"Password match: {check_password(password, user.password)}")
    
        if username and password:
            user = authenticate(request, username=username, password=password)
            print("Authenticated: ", user)

        if user is not None:
            login(request, user)
            return render(user, 'home.html')

    return render(request, 'login.html')

def signin_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            create_user(username, password)
            print("Authenticated: ", user)

        if user is not None:
            login(request, user)
            return render(user, 'home.html')

    return render(request, 'login.html')



def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
def home_page(request):
    # from django.template.context_processors import auth
    
    # # Check what auth context processor would add
    # auth_context = auth(request)
    # print(f"Auth context: {auth_context}")

    print("USer: ", request.user)
    print(f"Is authenticated: {request.user.is_authenticated}")
    context ={
        'user': request.user
    }
    return render(request, 'home.html', context)
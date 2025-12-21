"""
URL configuration for content_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from users.views import login_page, signin_page, logout_page, home_page
from posts.views import PostView
from likes.views import like_post


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login'),
    path('signin/', signin_page, name='signin'),
    path('logout/', logout_page, name='logout'),            
    path('home/', home_page, name='home'),   
    
    path('posts/', PostView.as_view(), name='posts'),
    path('like_posts/', like_post, name='like_post'),   
                                       
    path('', login_page),        
]

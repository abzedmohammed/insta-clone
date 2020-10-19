from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http  import HttpResponse
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .forms import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.conf import settings 
from django.core.mail import send_mail 
from django.urls import reverse

@login_required
def index(request):
    posts = Post.objects.all().filter(date__lte=timezone.now()).order_by('-date')
    
    return render(request, 'index.html', {'posts':posts})

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    users = Follow.follower.all()
    posts = Post.objects.filter(user=user).order_by("-date")
    
    return render(request,'profile.html', {'user':user, 'profile':profile, 'users':users, 'posts':posts})

@login_required
def timeline(request):
    user = request.user
    stream = Stream.objects.filter(user=user)
    posts = Post.objects.all().filter(date__lte=timezone.now()).order_by('-date')
    
    group_ids = []
    
    for items in stream:
        group_ids.append(items.post_id)
        
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-date')
    
    return render(request, 'timeline.html', {'posts':posts, 'stream':stream,'post_items':post_items})

@login_required
def single_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'single_post.html', {'post':post})    

@login_required
def add_image(request):
    user = request.user
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return redirect('/')
        else:
            return False
    
    return render(request, 'add_image.html', {'form':ImageForm,})

@login_required
def like(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.like
    
    liked = Likes.objects.filter(user=user, post=post).count()
    
    if not liked:
        like = Likes.objects.create(user=user,post=post)
        
        current_likes = current_likes + 1
        
    else:
        Likes.objects.filter(user=user,post=post).delete()
        current_likes = current_likes - 1
        
    post.like = current_likes
    post.save() 
    
    return HttpResponseRedirect(reverse('MainPage'))       
     

def search_results(request):
    
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

# def welcome_email(request):
#     if request.method == 'POST':
#         username = request.POST('username')
#         password = request.POST('password')
#         email = request.POST('email')
#         user = User.objects.create_user(
#             username = username,
#             email = email,
#             password = password,
#         )
        
#         login(request, user)
        
#         subject = 'welcome to Insta Clone'
#         message = f'Hi {user.username}, thank you for registering in Insta Clone. Enjoy the app..'
#         email_from = settings.EMAIL_HOST_USER 
#         recipient_list = [user.email] 
#         send_mail( subject, message, email_from, recipient_list ) 

#         return redirect('/')
#     return render(request, 'django_registration/registration_form.html', {'form': form})

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    
    return render(request, '/django_registration/login.html')
        
@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')
    
    
